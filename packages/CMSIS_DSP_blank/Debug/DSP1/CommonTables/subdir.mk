################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/CommonTables.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/CommonTablesF16.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_common_tables.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_common_tables_f16.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_const_structs.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_const_structs_f16.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_mve_tables.c \
/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_mve_tables_f16.c 

OBJS += \
./DSP1/CommonTables/CommonTables.o \
./DSP1/CommonTables/CommonTablesF16.o \
./DSP1/CommonTables/arm_common_tables.o \
./DSP1/CommonTables/arm_common_tables_f16.o \
./DSP1/CommonTables/arm_const_structs.o \
./DSP1/CommonTables/arm_const_structs_f16.o \
./DSP1/CommonTables/arm_mve_tables.o \
./DSP1/CommonTables/arm_mve_tables_f16.o 

C_DEPS += \
./DSP1/CommonTables/CommonTables.d \
./DSP1/CommonTables/CommonTablesF16.d \
./DSP1/CommonTables/arm_common_tables.d \
./DSP1/CommonTables/arm_common_tables_f16.d \
./DSP1/CommonTables/arm_const_structs.d \
./DSP1/CommonTables/arm_const_structs_f16.d \
./DSP1/CommonTables/arm_mve_tables.d \
./DSP1/CommonTables/arm_mve_tables_f16.d 


# Each subdirectory must supply rules for building sources it contributes
DSP1/CommonTables/CommonTables.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/CommonTables.c DSP1/CommonTables/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP1/CommonTables/CommonTablesF16.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/CommonTablesF16.c DSP1/CommonTables/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP1/CommonTables/arm_common_tables.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_common_tables.c DSP1/CommonTables/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP1/CommonTables/arm_common_tables_f16.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_common_tables_f16.c DSP1/CommonTables/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP1/CommonTables/arm_const_structs.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_const_structs.c DSP1/CommonTables/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP1/CommonTables/arm_const_structs_f16.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_const_structs_f16.c DSP1/CommonTables/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP1/CommonTables/arm_mve_tables.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_mve_tables.c DSP1/CommonTables/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
DSP1/CommonTables/arm_mve_tables_f16.o: /Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Source/CommonTables/arm_mve_tables_f16.c DSP1/CommonTables/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/Include -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS-DSP/1.16.2/PrivateInclude -I/Users/nbaldicc/STM32Cube/Repository/Packs/ARM/CMSIS/6.1.0/CMSIS/Core/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-DSP1-2f-CommonTables

clean-DSP1-2f-CommonTables:
	-$(RM) ./DSP1/CommonTables/CommonTables.cyclo ./DSP1/CommonTables/CommonTables.d ./DSP1/CommonTables/CommonTables.o ./DSP1/CommonTables/CommonTables.su ./DSP1/CommonTables/CommonTablesF16.cyclo ./DSP1/CommonTables/CommonTablesF16.d ./DSP1/CommonTables/CommonTablesF16.o ./DSP1/CommonTables/CommonTablesF16.su ./DSP1/CommonTables/arm_common_tables.cyclo ./DSP1/CommonTables/arm_common_tables.d ./DSP1/CommonTables/arm_common_tables.o ./DSP1/CommonTables/arm_common_tables.su ./DSP1/CommonTables/arm_common_tables_f16.cyclo ./DSP1/CommonTables/arm_common_tables_f16.d ./DSP1/CommonTables/arm_common_tables_f16.o ./DSP1/CommonTables/arm_common_tables_f16.su ./DSP1/CommonTables/arm_const_structs.cyclo ./DSP1/CommonTables/arm_const_structs.d ./DSP1/CommonTables/arm_const_structs.o ./DSP1/CommonTables/arm_const_structs.su ./DSP1/CommonTables/arm_const_structs_f16.cyclo ./DSP1/CommonTables/arm_const_structs_f16.d ./DSP1/CommonTables/arm_const_structs_f16.o ./DSP1/CommonTables/arm_const_structs_f16.su ./DSP1/CommonTables/arm_mve_tables.cyclo ./DSP1/CommonTables/arm_mve_tables.d ./DSP1/CommonTables/arm_mve_tables.o ./DSP1/CommonTables/arm_mve_tables.su ./DSP1/CommonTables/arm_mve_tables_f16.cyclo ./DSP1/CommonTables/arm_mve_tables_f16.d ./DSP1/CommonTables/arm_mve_tables_f16.o ./DSP1/CommonTables/arm_mve_tables_f16.su

.PHONY: clean-DSP1-2f-CommonTables

