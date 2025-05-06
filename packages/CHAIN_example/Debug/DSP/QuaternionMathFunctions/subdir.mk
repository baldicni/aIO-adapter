################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion2rotation_f32.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_conjugate_f32.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_inverse_f32.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_norm_f32.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_normalize_f32.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_product_f32.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_product_single_f32.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_rotation2quaternion_f32.c 

OBJS += \
./DSP/QuaternionMathFunctions/arm_quaternion2rotation_f32.o \
./DSP/QuaternionMathFunctions/arm_quaternion_conjugate_f32.o \
./DSP/QuaternionMathFunctions/arm_quaternion_inverse_f32.o \
./DSP/QuaternionMathFunctions/arm_quaternion_norm_f32.o \
./DSP/QuaternionMathFunctions/arm_quaternion_normalize_f32.o \
./DSP/QuaternionMathFunctions/arm_quaternion_product_f32.o \
./DSP/QuaternionMathFunctions/arm_quaternion_product_single_f32.o \
./DSP/QuaternionMathFunctions/arm_rotation2quaternion_f32.o 

C_DEPS += \
./DSP/QuaternionMathFunctions/arm_quaternion2rotation_f32.d \
./DSP/QuaternionMathFunctions/arm_quaternion_conjugate_f32.d \
./DSP/QuaternionMathFunctions/arm_quaternion_inverse_f32.d \
./DSP/QuaternionMathFunctions/arm_quaternion_norm_f32.d \
./DSP/QuaternionMathFunctions/arm_quaternion_normalize_f32.d \
./DSP/QuaternionMathFunctions/arm_quaternion_product_f32.d \
./DSP/QuaternionMathFunctions/arm_quaternion_product_single_f32.d \
./DSP/QuaternionMathFunctions/arm_rotation2quaternion_f32.d 


# Each subdirectory must supply rules for building sources it contributes
DSP/QuaternionMathFunctions/arm_quaternion2rotation_f32.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion2rotation_f32.c DSP/QuaternionMathFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP/QuaternionMathFunctions/arm_quaternion_conjugate_f32.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_conjugate_f32.c DSP/QuaternionMathFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP/QuaternionMathFunctions/arm_quaternion_inverse_f32.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_inverse_f32.c DSP/QuaternionMathFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP/QuaternionMathFunctions/arm_quaternion_norm_f32.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_norm_f32.c DSP/QuaternionMathFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP/QuaternionMathFunctions/arm_quaternion_normalize_f32.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_normalize_f32.c DSP/QuaternionMathFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP/QuaternionMathFunctions/arm_quaternion_product_f32.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_product_f32.c DSP/QuaternionMathFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP/QuaternionMathFunctions/arm_quaternion_product_single_f32.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_quaternion_product_single_f32.c DSP/QuaternionMathFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP/QuaternionMathFunctions/arm_rotation2quaternion_f32.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/QuaternionMathFunctions/arm_rotation2quaternion_f32.c DSP/QuaternionMathFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-DSP-2f-QuaternionMathFunctions

clean-DSP-2f-QuaternionMathFunctions:
	-$(RM) ./DSP/QuaternionMathFunctions/arm_quaternion2rotation_f32.cyclo ./DSP/QuaternionMathFunctions/arm_quaternion2rotation_f32.d ./DSP/QuaternionMathFunctions/arm_quaternion2rotation_f32.o ./DSP/QuaternionMathFunctions/arm_quaternion2rotation_f32.su ./DSP/QuaternionMathFunctions/arm_quaternion_conjugate_f32.cyclo ./DSP/QuaternionMathFunctions/arm_quaternion_conjugate_f32.d ./DSP/QuaternionMathFunctions/arm_quaternion_conjugate_f32.o ./DSP/QuaternionMathFunctions/arm_quaternion_conjugate_f32.su ./DSP/QuaternionMathFunctions/arm_quaternion_inverse_f32.cyclo ./DSP/QuaternionMathFunctions/arm_quaternion_inverse_f32.d ./DSP/QuaternionMathFunctions/arm_quaternion_inverse_f32.o ./DSP/QuaternionMathFunctions/arm_quaternion_inverse_f32.su ./DSP/QuaternionMathFunctions/arm_quaternion_norm_f32.cyclo ./DSP/QuaternionMathFunctions/arm_quaternion_norm_f32.d ./DSP/QuaternionMathFunctions/arm_quaternion_norm_f32.o ./DSP/QuaternionMathFunctions/arm_quaternion_norm_f32.su ./DSP/QuaternionMathFunctions/arm_quaternion_normalize_f32.cyclo ./DSP/QuaternionMathFunctions/arm_quaternion_normalize_f32.d ./DSP/QuaternionMathFunctions/arm_quaternion_normalize_f32.o ./DSP/QuaternionMathFunctions/arm_quaternion_normalize_f32.su ./DSP/QuaternionMathFunctions/arm_quaternion_product_f32.cyclo ./DSP/QuaternionMathFunctions/arm_quaternion_product_f32.d ./DSP/QuaternionMathFunctions/arm_quaternion_product_f32.o ./DSP/QuaternionMathFunctions/arm_quaternion_product_f32.su ./DSP/QuaternionMathFunctions/arm_quaternion_product_single_f32.cyclo ./DSP/QuaternionMathFunctions/arm_quaternion_product_single_f32.d ./DSP/QuaternionMathFunctions/arm_quaternion_product_single_f32.o ./DSP/QuaternionMathFunctions/arm_quaternion_product_single_f32.su ./DSP/QuaternionMathFunctions/arm_rotation2quaternion_f32.cyclo ./DSP/QuaternionMathFunctions/arm_rotation2quaternion_f32.d ./DSP/QuaternionMathFunctions/arm_rotation2quaternion_f32.o ./DSP/QuaternionMathFunctions/arm_rotation2quaternion_f32.su

.PHONY: clean-DSP-2f-QuaternionMathFunctions

