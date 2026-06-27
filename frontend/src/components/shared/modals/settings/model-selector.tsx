import {
  Autocomplete,
  AutocompleteItem,
} from "@heroui/react";
import React from "react";
import { useTranslation } from "react-i18next";
import { I18nKey } from "#/i18n/declaration";
import { extractModelAndProvider } from "#/utils/extract-model-and-provider";
import { cn } from "#/utils/utils";
import { useProviderModels } from "#/hooks/query/use-provider-models";

const XAI_PROVIDER = "xai";

interface ModelSelectorProps {
  isDisabled?: boolean;
  currentModel?: string;
  onChange?: (provider: string | null, model: string | null) => void;
  onDefaultValuesChanged?: (
    provider: string | null,
    model: string | null,
  ) => void;
  wrapperClassName?: string;
  labelClassName?: string;
}

export function ModelSelector({
  isDisabled,
  currentModel,
  onChange,
  onDefaultValuesChanged,
  wrapperClassName,
  labelClassName,
}: ModelSelectorProps) {
  const [selectedModel, setSelectedModel] = React.useState<string | null>(null);

  const {
    data: providerModels = [],
    isLoading: isLoadingModels,
    error: modelsError,
  } = useProviderModels(XAI_PROVIDER);

  const dropdownModels = React.useMemo(
    () => providerModels.filter((m) => !m.hidden),
    [providerModels],
  );

  const isSelectedModelUnavailable = React.useMemo(
    () =>
      !!selectedModel &&
      !isLoadingModels &&
      !modelsError &&
      providerModels.length > 0 &&
      !providerModels.some((m) => m.name === selectedModel),
    [selectedModel, isLoadingModels, modelsError, providerModels],
  );

  React.useEffect(() => {
    if (currentModel) {
      const { model } = extractModelAndProvider(currentModel);
      setSelectedModel(model);
      onDefaultValuesChanged?.(XAI_PROVIDER, model);
    }
  }, [currentModel, onDefaultValuesChanged]);

  const handleChangeModel = (model: string) => {
    setSelectedModel(model);
    onChange?.(XAI_PROVIDER, model);
  };

  const { t } = useTranslation();

  return (
    <div
      className={cn(
        "flex flex-col w-full max-w-[680px]",
        wrapperClassName,
      )}
    >
      <fieldset className="flex flex-col gap-2.5 w-full">
        <label className={cn("text-sm", labelClassName)}>
          {t(I18nKey.LLM$MODEL)}
        </label>
        <Autocomplete
          data-testid="llm-model-input"
          isRequired
          isVirtualized={false}
          isLoading={isLoadingModels}
          name="llm-model-input"
          aria-label={t(I18nKey.LLM$MODEL)}
          placeholder={t(I18nKey.LLM$SELECT_MODEL_PLACEHOLDER)}
          isClearable={false}
          onSelectionChange={(e) => {
            if (e?.toString()) handleChangeModel(e.toString());
          }}
          isDisabled={isDisabled}
          selectedKey={selectedModel}
          defaultSelectedKey={selectedModel ?? undefined}
          classNames={{
            popoverContent: "bg-tertiary rounded-xl border border-[#717888]",
          }}
          inputProps={{
            classNames: {
              inputWrapper:
                "bg-tertiary border border-[#717888] h-10 w-full rounded-sm p-2 placeholder:italic",
            },
          }}
        >
          {dropdownModels.map((model) => (
            <AutocompleteItem
              data-testid={`model-item-${model.name}`}
              key={model.name}
            >
              {model.name}
            </AutocompleteItem>
          ))}
        </Autocomplete>
        {modelsError && (
          <p data-testid="models-error" className="text-danger text-xs">
            {t(I18nKey.CONFIGURATION$ERROR_FETCH_MODELS)}
          </p>
        )}
        {isSelectedModelUnavailable && (
          <p
            data-testid="model-unavailable-warning"
            className="text-yellow-400 text-xs"
          >
            {t(I18nKey.SETTINGS$MODEL_NO_LONGER_AVAILABLE)}
          </p>
        )}
      </fieldset>
    </div>
  );
}
