from pydantic import BaseModel
from typing import Optional, List, ClassVar, Dict
from datetime import datetime



class ProductSalesSchema(BaseModel):

    def product_validator(self, product_code: Optional[int] = None) -> int:
        
        if product_code is None:
            return None
        
        if type(product_code) == int:
            return product_code
        else:
            raise ValueError("valores em números inteiros")


    def store_validator(self, store_code: Optional[str] = None) -> str:
        
        if store_code is None:
            return None
        
        elif type(store_code) == int:
            store_code = str(store_code)
            return store_code
        else:
            raise ValueError("valores em números inteiros")


    def data_validator(self, data_range: Optional[List[str]] = None) -> Optional[List]:

        if data_range is None:
            return None

        if not isinstance(data_range, list):
            raise ValueError("data_range precisa ser uma lista")
        
        if len(data_range) != 2:
            raise ValueError("data_range pracisa ter duas posiçoes")
        
        validate_data = []
        for data_inf in data_range:

            if data_inf is None:
                validate_data.append(None)
                continue

            try:
                data_obj = datetime.strptime(data_inf, "%Y-%m-%d").date()
                validate_data.append(data_obj)
            except ValueError:
                raise ValueError(f"Data {data_inf} fora do formato")
        
        if validate_data[0] and validate_data[1]:
            if validate_data[0] > validate_data[1]:
                raise ValueError(f"Data inicial - {validate_data[0]} maior que Data final - {validate_data[1]}")

        if validate_data[0] is None and validate_data[1] is None:
            return None


        return validate_data

    COLUMN_MAP: ClassVar[Dict[str, str]] = {
        "product_code": "PRODUCT_CODE",
        "store_code": "STORE_CODE",
        "data_range": "DATE"
    }