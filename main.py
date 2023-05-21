import openai

from db_connector import Connector
from db_queries import extract_table_metadata, exec_query

if __name__ == '__main__':
    openai.api_key = ''

    connector = Connector(host='localhost', port=5432, database='demo', user='moshe', password='password')
    connector.connect()

    metadata = extract_table_metadata(conn=connector.conn)

    while True:
        requirement = input("Enter your requirement/question: ")

        messages = [
            {"role": "system", "content": f"given the next sql scheme, and requirement, return a clean sql syntax "
                                          f"just an sql. without nothing else"
                                          f" if you can't produce a query write an Error: <error_goes_here> \n"
                                          f"requirement: {requirement} \n"
                                          f"{metadata}"},
        ]

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        answer = completion.choices[0].message.content

        while True:
            try:
                result = exec_query(conn=connector.conn, query=answer)
                print(f'AI says: Here is the query based on your requirement\n'
                      f'***************\n'
                      f'***************\n'
                      f'{answer} \n'
                      f'***************\n'
                      f'***************\n')

                print(f'AI says: Here is the answer\n'
                      f'***************\n'
                      f'***************\n'
                      f'{result} \n'
                      f'***************\n'
                      f'***************\n')
                break

            except SyntaxError as e:
                print(f'System says: Error\n'
                      f'***************\n'
                      f'***************\n'
                      f'{answer} \n'
                      f'***************\n'
                      f'***************\n')
                messages.append(e)
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                answer = completion.choices[0].message.content

        continue_prompt = input("Do you want to ask another question? (y/n): ")
        if continue_prompt.lower() != "y":
            break

    connector.conn.close()

"""
given the next sql scheme, and requirement, return a clean sql syntax just an sql. without nothing else if you can't produce a query write an Error: <error_goes_here> 
requirement: which user order the most ? 
Table: users 
- Column: user_id, Data Type: integer, Constraint: PK 
- Column: name, Data Type: text, Constraint:  
- Column: email, Data Type: text, Constraint:  
Table: orders 
- Column: order_id, Data Type: integer, Constraint: PK 
- Column: user_id, Data Type: integer, Constraint: FK: users.user_id 
- Column: order_date, Data Type: date, Constraint:  
Table: order_items 
- Column: order_item_id, Data Type: integer, Constraint: PK 
- Column: order_id, Data Type: integer, Constraint: FK: orders.order_id 
- Column: product_id, Data Type: integer, Constraint: FK: products.product_id 
- Column: quantity, Data Type: integer, Constraint:  
Table: products 
- Column: product_id, Data Type: integer, Constraint: PK 
- Column: price, Data Type: numeric, Constraint:  
- Column: name, Data Type: text, Constraint:  
- Column: description, Data Type: text, Constraint:  
Table: reviews 
- Column: review_id, Data Type: integer, Constraint: PK 
- Column: user_id, Data Type: integer, Constraint: FK: users.user_id 
- Column: product_id, Data Type: integer, Constraint: FK: products.product_id 
- Column: rating, Data Type: integer, Constraint:  
- Column: comment, Data Type: text, Constraint:  
Table: player 
- Column: price, Data Type: numeric, Constraint:  
- Column: age, Data Type: integer, Constraint:  
- Column: speed, Data Type: integer, Constraint:  
- Column: shot_speed, Data Type: integer, Constraint:  
- Column: jump_height, Data Type: integer, Constraint:  
- Column: country, Data Type: character varying, Constraint:  
- Column: position, Data Type: character varying, Constraint:  
- Column: player_name, Data Type: character varying, Constraint: PK 
Table: games 
- Column: location, Data Type: character varying, Constraint:  
- Column: score, Data Type: character varying, Constraint:  
- Column: best_player, Data Type: character varying, Constraint: FK: player.player_name 

"""
