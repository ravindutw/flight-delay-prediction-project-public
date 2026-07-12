-- Flight data

select * from flight_data limit 10;

select arr_delay_group, COUNT(arr_delay_group) as count_per_group from flight_data group by arr_delay_group;

select distinct cancellation_code from flight_data;

select cancellation_code, COUNT(cancellation_code) as cancellation_code_count from flight_data group by cancellation_code;

select distinct flights from flight_data;

select distinct total_add_gtime from flight_data;



-- Weather data

select distinct alti, count(alti) from weather_data group by alti;;

select * from weather_data limit 10;

select distinct sknt, count(sknt) from weather_data group by sknt;

select count(alti) as _count from weather_data where alti = 'M';