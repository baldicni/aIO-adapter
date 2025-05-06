################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include Drivers/STM32F7xx_HAL_Driver/Src/subdir.mk
-include DSP/WindowFunctions/subdir.mk
-include DSP/TransformFunctions/subdir.mk
-include DSP/SupportFunctions/subdir.mk
-include DSP/StatisticsFunctions/subdir.mk
-include DSP/SVMFunctions/subdir.mk
-include DSP/QuaternionMathFunctions/subdir.mk
-include DSP/MatrixFunctions/subdir.mk
-include DSP/InterpolationFunctions/subdir.mk
-include DSP/FilteringFunctions/subdir.mk
-include DSP/FastMathFunctions/subdir.mk
-include DSP/DistanceFunctions/subdir.mk
-include DSP/ControllerFunctions/subdir.mk
-include DSP/ComplexMathFunctions/subdir.mk
-include DSP/CommonTables/subdir.mk
-include DSP/BayesFunctions/subdir.mk
-include DSP/BasicMathFunctions/subdir.mk
-include Core/Startup/subdir.mk
-include Core/Src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := CHAIN_example
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
CHAIN_example.elf \

MAP_FILES += \
CHAIN_example.map \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
CHAIN_example.list \


# All Target
all: main-build

# Main-build Target
main-build: CHAIN_example.elf secondary-outputs

# Tool invocations
CHAIN_example.elf CHAIN_example.map: $(OBJS) $(USER_OBJS) /Users/nbaldicc/Desktop/JAPworkspace/CHAIN_example/STM32F767ZITX_FLASH.ld makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-gcc -o "CHAIN_example.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m7 -T"/Users/nbaldicc/Desktop/JAPworkspace/CHAIN_example/STM32F767ZITX_FLASH.ld" --specs=nosys.specs -Wl,-Map="CHAIN_example.map" -Wl,--gc-sections -static --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -Wl,--start-group -lc -lm -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

CHAIN_example.list: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "CHAIN_example.list"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) CHAIN_example.elf CHAIN_example.list CHAIN_example.map default.size.stdout
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents main-build fail-specified-linker-script-missing warn-no-linker-script-specified

-include ../makefile.targets
