# SELECIONE AS VARIÁVEIS DE INTERESSE

dataset = "derived-era5-land-daily-statistics" # Dataset com valores diários já processados (Média).
variaveis = [
                # # TEMPERATURA
                # "2m_dewpoint_temperature",
                # "2m_temperature",
                "skin_temperature",
                # "soil_temperature_level_1",
                # "soil_temperature_level_2",
                # "soil_temperature_level_3",
                # "soil_temperature_level_4",

                # # LAGOS
                # "lake_bottom_temperature",
                # "lake_ice_depth",
                # "lake_ice_temperature",
                # "lake_mix_layer_depth",
                # "lake_mix_layer_temperature",
                # "lake_shape_factor",
                # "lake_total_layer_temperature",

                # # NEVE
                # "snow_albedo",
                # "snow_cover",
                # "snow_density",
                # "snow_depth",
                # "snow_depth_water_equivalent",
                # "temperature_of_snow_layer",

                # # ÁGUA NO SOLO
                # "skin_reservoir_content",
                # "volumetric_soil_water_layer_1",
                # "volumetric_soil_water_layer_2",
                # "volumetric_soil_water_layer_3",
                # "volumetric_soil_water_layer_4",

                # # VENTO E PRESSÃO
                # "10m_u_component_of_wind",
                # "10m_v_component_of_wind",
                "surface_pressure",

                # # VEGETAÇÃO E ALBEDO (ALBEDO = CAPACIDADE DE REFLETIR A RADIAÇÃO SOLAR)
                # "leaf_area_index_high_vegetation",
                # "leaf_area_index_low_vegetation",

                # # ALBEDO E PREVISÃO
                # "forecast_albedo"
            ]
ano = "2025" # 1950 - Atual
mes = ["01"] # 01 - 12
dia = ["01", "02", "03"] # Selecionar dias de interesse. Verificar mês com 31 dias.
estatistica_diaria = "daily_mean" # "daily_minimum", "daily_maximum"
tempo_UTC = "utc-03:00" # Horário de Brasília
frequencia = "1_hourly" # "3_hourly", "6_hourly"