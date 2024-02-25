from Tools.services.features import Service


class shopping(Service):

    @property
    def service(self):
        return "shopping"
    
    @property
    def tools(self):
        return   {
      "name": "extractShoppingDetail",
      "description": "Extract shopping detail from the user prompt",
      "parameters": {
        "type": "object",
        "properties": {
          "item": {
            "type": "string",
            "description": "The item name"
          },
          "amount": {
            "type": "number",
            "description": "The amount of the item"
          },
          "brand": {
            "type": "string",
            "description": "The brand of the item"
          },
          "price": {
            "type": "number",
            "description": "The price of the item"
          }
        },
        "required": ["query"]
      }
    }