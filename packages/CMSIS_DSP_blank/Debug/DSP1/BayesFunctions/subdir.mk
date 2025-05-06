################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/BayesFunctions/BayesFunctions.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/BayesFunctions/BayesFunctionsF16.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/BayesFunctions/arm_gaussian_naive_bayes_predict_f16.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/BayesFunctions/arm_gaussian_naive_bayes_predict_f32.c 

OBJS += \
./DSP1/BayesFunctions/BayesFunctions.o \
./DSP1/BayesFunctions/BayesFunctionsF16.o \
./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f16.o \
./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f32.o 

C_DEPS += \
./DSP1/BayesFunctions/BayesFunctions.d \
./DSP1/BayesFunctions/BayesFunctionsF16.d \
./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f16.d \
./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f32.d 


# Each subdirectory must supply rules for building sources it contributes
DSP1/BayesFunctions/BayesFunctions.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/BayesFunctions/BayesFunctions.c DSP1/BayesFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP1/BayesFunctions/BayesFunctionsF16.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/BayesFunctions/BayesFunctionsF16.c DSP1/BayesFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f16.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/BayesFunctions/arm_gaussian_naive_bayes_predict_f16.c DSP1/BayesFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f32.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/BayesFunctions/arm_gaussian_naive_bayes_predict_f32.c DSP1/BayesFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-DSP1-2f-BayesFunctions

clean-DSP1-2f-BayesFunctions:
	-$(RM) ./DSP1/BayesFunctions/BayesFunctions.cyclo ./DSP1/BayesFunctions/BayesFunctions.d ./DSP1/BayesFunctions/BayesFunctions.o ./DSP1/BayesFunctions/BayesFunctions.su ./DSP1/BayesFunctions/BayesFunctionsF16.cyclo ./DSP1/BayesFunctions/BayesFunctionsF16.d ./DSP1/BayesFunctions/BayesFunctionsF16.o ./DSP1/BayesFunctions/BayesFunctionsF16.su ./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f16.cyclo ./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f16.d ./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f16.o ./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f16.su ./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f32.cyclo ./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f32.d ./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f32.o ./DSP1/BayesFunctions/arm_gaussian_naive_bayes_predict_f32.su

.PHONY: clean-DSP1-2f-BayesFunctions

