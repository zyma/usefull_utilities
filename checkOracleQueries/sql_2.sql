select c.*, r.country, r.country_id 
from ODI_DEMO.SRC_CITY c
  join odi_demo.src_region r on (c.region_id = r.region_id)
