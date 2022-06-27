from flask import Flask, jsonify
import sqlite3

def main():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['DEBUG'] = True

    def db_connect(query):
        con = sqlite3.connect('netflix.db')
        cursor = con.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        con.close()
        return result



    @app.route('/movie/<title>')
    def search_by_title(title):
        query = f"""
            SELECT
                title
                , country
                , release_year
                , listed_in AS genre
                , description
            FROM netflix
            WHERE title = '{title}'
            ORDER BY release_year DESC
            LIMIT 1             
        """
        response = db_connect(query)[0]
        response_json = {
            'title': response[0],
            'country': response[1],
            'release_year': response[2],
            'listed_in': response[3],
            'description': response[4],
        }
        return jsonify(response_json)



    @app.route('/movie/<int:start>/to/<int:end>')
    def search_by_period(start, end):
        query = f"""
            SELECT
                title
                , release_year
            FROM netflix
            WHERE release_year BETWEEN {start} AND {end}
            ORDER BY release_year 
            LIMIT 100            
        """
        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'release_year': film[1]
            })
        return jsonify(response_json)



    @app.route('/rating/<group>')
    def search_by_rating(group):
        levels = {
            'children': ['G'],
            'family': ['G', 'PG', 'PG-13'],
            'adult': ['R', 'NC-17']
        }
        if group in levels:
            level = '\", \"'.join(levels[group])
            level = f'\"{level}\"'
        else:
            return jsonify ([])

        query = f"""
            SELECT
                title
                , rating
                ,description                        
            FROM netflix
            WHERE rating IN ({level})          
        """
        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'rating': film[1],
                'description': film[2]
            })
        return jsonify(response_json)

    @app.route('/genre/<genre>')
    def search_by_genre(genre):
        query = f"""
            SELECT
                title
                , description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10            
        """
        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'description': film[1]
            })
        return jsonify(response_json)

   # app.run(debug=True)

    def get_actors(self, name1, name2):
        query = f"""
            SELECT "cast" FROM netflix
            WHERE "cast" LIKE '%{name1}%' AND "cast" LIKE '%{name2}%'
        """
        response = db_connect(query)
        actors = []
        for cast in response:
            actors.extend(cast[0].split(', '))
        result = []
        for i in actors:
            if i not in [name1, name2]:
                if actors.count(i) > 2:
                    result.append(i)
        result = self.db_connect(query)
        print(result)


    def get_films(self, type_film, release_year, genre):
        query = f"""
                 SELECT title
                 , description
                 , "type" 
                 FROM netflix
                 WHERE "type" = '{type_film}' 
                 AND release_year = '{release_year}'
                 AND listed_in LIKE '%{genre}%'
             """
        response = self.db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'description': film[1],
                'type': film[2]
            })
        return(response_json)


    get_films()
    get_actors()

if __name__ == '__main__':
    main()