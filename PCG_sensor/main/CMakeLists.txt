set(req driver)
idf_component_register(SRCS "i2s_test.c"
                       INCLUDE_DIRS "." 
                       REQUIRES ${req}) 