/**
 * \name ECG signal measure
 * \note Chi do raw data, khong can bo loc
 */
#include <stdio.h>
#include <stdint.h>
#include "esp_err.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/adc.h"

#define ADC_CHANNEL ADC_CHANNEL_6 //GPIO34
#define ADC_UNIT ADC_UNIT_1
#define ADC_ATTEN ADC_ATTEN_DB_12 //Tang pham vi do 
#define ADC_WIDTH ADC_WIDTH_BIT_12
#define ADC_SAMPLE_RATE 100

static const char *TAG = "ADC";
TaskHandle_t readADTask_handle = NULL;


void adc_configure(){
  adc1_config_width(ADC_WIDTH);
  adc1_config_channel_atten(ADC_CHANNEL, ADC_ATTEN); //Suy hao
  ESP_LOGI(TAG, "ADC Configured: Channel: %d, Attenuation: %d", ADC_CHANNEL, ADC_ATTEN);
}

void read_AD8232(void *pvParameter){
  adc_configure();
  ESP_LOGI(TAG, "Bat dau doc cam bien AD8232");

  while(true){
    int sample = adc1_get_raw(ADC_CHANNEL);
    printf("%d\n", sample);
    vTaskDelay(pdMS_TO_TICKS(1000 / ADC_SAMPLE_RATE)); //10ms - Tan so lay mau cua ADC duoc the hien qua ham nay
  }
}

void app_main(void){
  xTaskCreatePinnedToCore(read_AD8232, "Read AD8323", 1024 * 4, NULL, 5, &readADTask_handle, 1);
}
