from Settings import settings
queries = {
    "create_db_and_tables": (
             f"""CREATE DATABASE {settings['db_creds']['db']};""",
             """CREATE TABLE IF NOT EXISTS business_info (
                        business_id BIGSERIAL PRIMARY KEY NOT NULL,
                        name VARCHAR(50),
                        phone VARCHAR(20), 
                        price_range INTEGER,
                        year_in_business INTEGER,
                        amenities text[],
                        categories text[],
                        city_name VARCHAR(50),
                        city_code VARCHAR(30),
                        zip_code INTEGER,
                        updated_at TIMESTAMP,
                        CONSTRAINT business_info_name_unique UNIQUE (name)
                        );
                        CREATE TABLE IF NOT EXISTS access_info (
                        open_status VARCHAR(30),
                        website VARCHAR(200),
                        order_online VARCHAR(30),
                        updated_at TIMESTAMP,
                        business_id BIGINT REFERENCES business_info(business_id),                                                     
                        CONSTRAINT access_unique_id_fk UNIQUE (business_id)
                        );
                        CREATE TABLE IF NOT EXISTS yellowpage_info (
                        rating FLOAT,
                        rating_count INTEGER,
                        updated_at TIMESTAMP,
                        business_id BIGINT REFERENCES business_info(business_id),
                        CONSTRAINT yellowpage_unique_id_fk UNIQUE (business_id)
                        );
                        CREATE TABLE IF NOT EXISTS tripadvisor_info (
                        rating FLOAT,
                        rating_count INTEGER,
                        updated_at TIMESTAMP,
                        business_id BIGINT REFERENCES business_info(business_id),
                        CONSTRAINT tripadvisor_unique_id_fk UNIQUE (business_id)
                        );
                        CREATE TABLE IF NOT EXISTS foursquare_info (
                        rating FLOAT,
                        updated_at TIMESTAMP,
                        business_id BIGINT REFERENCES business_info(business_id),
                        CONSTRAINT foursquare_unique_id_fk UNIQUE (business_id)
                        );"""
    ),
    "upsert_into_tables": (
        """
        INSERT INTO business_info 
        (
        name, 
        phone,
        price_range, 
        year_in_business,
        amenities,
        categories,
        city_name,
        city_code,
        zip_code,
        updated_at 
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW()) 
        ON CONFLICT (name) 
        DO UPDATE SET
        phone=EXCLUDED.phone,
        price_range=EXCLUDED.price_range ,
        year_in_business=EXCLUDED.year_in_business,
        amenities=EXCLUDED.amenities,
        city_code=EXCLUDED.city_code,
        city_name=EXCLUDED.city_name,
        zip_code=EXCLUDED.zip_code,
        categories=EXCLUDED.categories,
        updated_at=EXCLUDED.updated_at
        RETURNING business_id
        ;  
        """,
        """
        INSERT INTO access_info 
        (           
        open_status ,
        website,
        order_online ,
        updated_at ,
        business_id           
        )
        VALUES (%s,%s,%s,NOW(),%s) 
        ON CONFLICT (business_id) 
        DO UPDATE SET
        open_status=EXCLUDED.open_status,
        website=EXCLUDED.website,
        order_online=EXCLUDED.order_online,
        updated_at=EXCLUDED.updated_at 
        ;      
        """,
        """
        INSERT INTO yellowpage_info 
        (
        rating ,
        rating_count ,
        updated_at ,
        business_id 
        ) 
        VALUES (%s,%s,NOW(),%s) 
        ON CONFLICT (business_id) 
        DO UPDATE SET
        rating=EXCLUDED.rating,
        rating_count=EXCLUDED.rating_count
        ;
        """,
        """
        INSERT INTO tripadvisor_info 
        (
        rating ,
        rating_count ,
        updated_at ,
        business_id 
        ) 
        VALUES (%s,%s,NOW(),%s) 
        ON CONFLICT (business_id) 
        DO UPDATE SET
        rating=EXCLUDED.rating,
        rating_count=EXCLUDED.rating_count,
        updated_at=EXCLUDED.updated_at
        ;
        """,
        """
        INSERT INTO foursquare_info 
        (
        rating ,
        updated_at , 
        business_id 
        ) 
        VALUES (%s,NOW(),%s) 
        ON CONFLICT (business_id) 
        DO UPDATE SET
        rating=EXCLUDED.rating ,
        updated_at=EXCLUDED.updated_at
        ;        
        """
    ),
    "select":
        """
        SELECT 
        business_info.name, 
        business_info.phone, 
        business_info.price_range,
        business_info.year_in_business,
        business_info.amenities,
        business_info.categories,
        business_info.city_name,
        business_info.city_code,
        business_info.zip_code,
        business_info.updated_at,
        access_info.open_status,
        access_info.website,
        access_info.order_online,
        yellowpage_info.rating,
        yellowpage_info.rating_count,
        tripadvisor_info.rating,
        tripadvisor_info.rating_count,
        foursquare_info.rating        
        FROM business_info
        JOIN access_info ON business_info.business_id = access_info.business_id
        JOIN yellowpage_info ON business_info.business_id = yellowpage_info.business_id
        JOIN tripadvisor_info ON business_info.business_id = tripadvisor_info.business_id
        JOIN foursquare_info ON business_info.business_id = foursquare_info.business_id
        ;
        """
}
