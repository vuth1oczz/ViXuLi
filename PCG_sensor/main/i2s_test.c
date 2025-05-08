/**
 * @note ADC cua inmp441 la 24-bit nhung van chuyen tu 32-bit(esp32 de xu ly hon) 
 * ve 24-bit cua inmp roi moi ep ve 16-bit chu khong lay truc tiep 24-bit
 * @author Luong Huu Phuc
 */
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "hal/gpio_types.h"
#include "driver/gpio.h"
#include "esp_log.h"

//Thu vien I2S
#include <driver/i2s_std.h> //API moi <- Dung cai nay
#include <driver/i2s_types_legacy.h>
#include "driver/i2s_types.h"
#include "driver/i2s_common.h"

#define TAG "INMP441"

//Pin cau hinh INMP441 (I2S Mode)
#define I2S_NUM I2S_NUM_0
#define I2S_SCK_PIN 32
#define I2S_WS_PIN 25
#define I2S_SD_PIN 33
#define SAMPLE_RATE 4000 //Tan so lay mau 4000Hz

/**
 * @note Sample rate cang cao thi dmaLen cung cang cao de tranh mat mau
 * @param dmaLen Tang len neu du lieu bi mat mau, CPU bi ngat nhieu ma khong quan tam den latency
 * ->Cang lon thi buffer_durations cang lau->Cang it mat mau->CPU xu ly it viec hon->Tre lai cao hon
 * @param dmaDesc So bo dac ta DMA, moi bo co the luu tru so byte = dmaLen 
 */
#define dmaDesc 6 //Bo dac ta DMA
#define dmaLen 128 //So bytes cua moi buffer
#define DMA_BUFFER_SIZE (dmaLen * dmaDesc) //So bytes cua buffer DMA cung cap cho = 768　

//Buffer de luu tru du lieu doc duoc tu buffer DMA
//Chuyen doi tu byte DMA sang so luong mau cua moi buffer 
int16_t buffer16[DMA_BUFFER_SIZE / sizeof(int32_t) * 3 / 2] = {0}; //288 samples (576 bytes) de luu duoc 3 bytes sau khi dich cua buffer32
int32_t buffer32[DMA_BUFFER_SIZE / sizeof(int32_t)] = {0}; //192 samples (768 bytes)

TaskHandle_t readINMP441_handle = NULL;

//Tao kenh rx
i2s_chan_handle_t rx_channel = NULL;        

//Cau hinh i2s std (I2S_std)
void i2s_install(void){
    ESP_LOGI(TAG, "Cau hinh kenh i2s...");

    //Cau hinh kenh rx cho i2s
    i2s_chan_config_t chan_cfg = {
        .id = I2S_NUM,
        .role = I2S_ROLE_MASTER,
        .dma_desc_num = dmaDesc, //6 * 128 = 768
        .dma_frame_num = dmaLen, //128 bytes
        .auto_clear = true, 
    };

    //Khoi tao RX channel va ktr loi
    ESP_ERROR_CHECK(i2s_new_channel(&chan_cfg, NULL, &rx_channel));

    //Cau hinh che do chuan i2s, API moi
    i2s_std_config_t std_cfg = {
        //Cau hinh clock
        .clk_cfg = {
            .sample_rate_hz = SAMPLE_RATE, //Tan so lay mau
            .clk_src = I2S_CLK_SRC_DEFAULT, //Nguon clock mac dinh
            /**
             * @param mclk_multiple cang tang thi do nhieu (jitter) cua CLK va WS cang giam => Do chinh xac du lieu cang cao    
             * Day la boi so cua master clock doi voi tan so lay mau 
             */
            .mclk_multiple = I2S_MCLK_MULTIPLE_512, //Boi cua 3 (384,768,..) de phu hop voi du lieu 24 bit
        },  
        //Cau hinh du lieu trong 1 frame
        .slot_cfg = {
            /**
             * @note De 32-bit width thi moi chu ki dem duoc 10 mau
             * nhung khi de xuong 24-bit width thi dem len 13 mau ???
             */
            .data_bit_width = I2S_DATA_BIT_WIDTH_32BIT, //So bit moi du lieu
            .slot_mode = I2S_SLOT_MODE_MONO, //Che do mono (thu/phat 1 kenh)
            .slot_bit_width = I2S_SLOT_BIT_WIDTH_32BIT, //So bit moi slot (moi kenh)
            .slot_mask = I2S_STD_SLOT_LEFT //Kenh du lieu trai
        },      
        //Cau hinh GPIO
        .gpio_cfg = {
            .bclk = I2S_SCK_PIN,
            .ws = I2S_WS_PIN, 
            .dout = I2S_PIN_NO_CHANGE, //Khong can output data
            .din = I2S_SD_PIN, //GPIO cho du lieu input
        }
    };
    //Khoi tao che do chuan 
    ESP_ERROR_CHECK(i2s_channel_init_std_mode(rx_channel, &std_cfg));
    //Bat kenh RX 
    ESP_ERROR_CHECK(i2s_channel_enable(rx_channel));
    ESP_LOGI(TAG, "I2S da duoc cau hinh thanh cong !");
}

void readINMP441data_task(void *pvParameters){ 
    i2s_install();
    ESP_LOGI(TAG, "Bat dau doc du lieu tu INMP441...");

    size_t bytes_read;
    while(true){
        vTaskDelay(1);
        esp_err_t ret = i2s_channel_read(rx_channel, &buffer32, sizeof(buffer32), &bytes_read, 100);
        if(ret == ESP_ERR_TIMEOUT){
            ESP_LOGE(TAG, "Timeout xay ra, bo qua frame loi:  %s", esp_err_to_name(ret));
            continue;
        } else if(ret != ESP_OK){   
            ESP_LOGE(TAG, "Loi khong xac dinh: %s", esp_err_to_name(ret));
            break;
        }

        int samplesRead = bytes_read / sizeof(int32_t); //Số mẫu đọc được (1 kênh) || dữ liệu int32_t = 4 bytes 
        for(size_t i = 0; i < samplesRead; i++){
            buffer16[i] = (int16_t)(buffer32[i] >> 8); //Raw data
            printf("\n%d", buffer16[i]);
        }
    }  
}

void app_main(void){ 
    xTaskCreatePinnedToCore(readINMP441data_task, "readINMP441", 1024 * 15, NULL, 5, &readINMP441_handle, 1);
}
