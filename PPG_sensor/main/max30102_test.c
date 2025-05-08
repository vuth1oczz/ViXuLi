#include <stdio.h>
#include <inttypes.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <string.h>
#include <esp_timer.h>
#include <esp_vfs_fat.h>
#include <freertos/ringbuf.h>

// Incluse MAX30102 driver
#include "../component/MAX30102/max30102.h"


TaskHandle_t readMAXTask_handle = NULL;
struct max30102_record record;
struct max30102_data data;
unsigned long red, ir;

/**
 * @brief Read data from MAX30102 and send to ring buffer
 * 
 * @param pvParameters 
 */
void max30102_test(void *pvParameters){
    i2c_dev_t dev;
    memset(&dev, 0, sizeof(i2c_dev_t));
    ESP_ERROR_CHECK(max30102_initDesc(&dev, 0, 21, 22));
    if(max30102_readPartID(&dev) == ESP_OK) {
        ESP_LOGI(__func__, "Found MAX30102!");
    }
    else {
        ESP_LOGE(__func__, "Not found MAX30102");
    }

    uint8_t powerLed = 0x1F; //Cuong do led, tieu thu 6.4mA
    uint8_t sampleAverage = 4; 
    uint8_t ledMode = 2;
    int sampleRate = 500; //Tan so lay mau cao thi kich thuoc BUFFER_SIZE cung phai thay doi de co thoi gian thuat toan xu ly cac mau
    int pulseWidth = 411; //Xung cang rong, dai thu duoc cang nhieu (18 bit)
    int adcRange = 16384; //14 bit ADC tieu thu 65.2pA moi LSB

    ESP_ERROR_CHECK(max30102_init(powerLed, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange, &record, &dev));
    max30102_clearFIFO(&dev);   
    while (1){
        max30102_check(&record, &dev); //Check the sensor, read up to 3 samples
        while (max30102_available(&record)) //do we have new data?
        {
            red = max30102_getFIFORed(&record);
            ir = max30102_getFIFOIR(&record);
            printf("%ld,%ld\n", red, ir);
            max30102_nextSample(&record); 
    }
}
}

void app_main(void){
    ESP_ERROR_CHECK(i2cdev_init()); 
    xTaskCreatePinnedToCore(max30102_test, "max30102_test", 1024 * 5, &readMAXTask_handle, 6, NULL, 0);
}
