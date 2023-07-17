from unittest import TestCase
from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        with app.app_context():
            db.drop_all()
            db.create_all()
            c1 = Cupcake(flavor='chocolate', size='large', rating=4, image= "<http://test.com/cupcake.jpg>")
            c2 = Cupcake(flavor='vanilla', size='medium', rating=3, image= "<http://test.com/cupcake.jpg>")
            db.session.add_all([c1, c2])
            db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()


    def test_list_cupcakes(self):
        with app.app_context():
            #session
            session = db.session
            cupcakes = session.query(Cupcake).all()
            self.assertEqual(len(cupcakes), 2)

            with app.test_client() as client:
                resp = client.get("/api/cupcakes")

                self.assertEqual(resp.status_code, 200)

                data = resp.json
                self.assertEqual(data, {
                    "cupcakes": [
                        {
                            "id": cupcakes[0].id,
                            "flavor": "chocolate",
                            "size": "large",
                            "rating": 4,
                            "image": "<http://test.com/cupcake.jpg>"
                        },
                        {
                            "id": cupcakes[1].id,
                            "flavor": "vanilla",
                            "size": "medium",
                            "rating": 3,
                            "image": "<http://test.com/cupcake.jpg>"
                        }
                    ]
                })


    def test_get_cupcake(self):
        with app.app_context():
            session = db.session
            cupcake = session.query(Cupcake).first()

        with app.test_client() as client:
            url = f"/api/cupcakes/{cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": cupcake.id,
                    "flavor": "chocolate",
                    "size": "large",
                    "rating": 4,
                    "image": "<http://test.com/cupcake.jpg>"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            c3 = Cupcake(flavor='berry', size='large', rating=8, image= "<http://test.com/cupcake.jpg>")
            url = "/api/cupcakes"
            resp = client.post(url, json=c3.serialize())

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "berry",
                    "size": "large",
                    "rating": 8,
                    "image": "<http://test.com/cupcake.jpg>"
                }
            })

            self.assertEqual(Cupcake.query.count(), 3)

    def test_update_cupcake(self):
        with app.app_context():
            session = db.session
            cupcake = session.query(Cupcake).first()

        with app.test_client() as client:
            url = f"/api/cupcakes/{cupcake.id}"
            resp = client.patch(url, json={"flavor": "new-flavor"})

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": cupcake.id,
                    "flavor": "new-flavor",
                    "size": "large",
                    "rating": 4,
                    "image": "<http://test.com/cupcake.jpg>"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def delete_cupcake(self):
        with app.app_context():
            session = db.session
            cupcake = session.query(Cupcake).first()
            
        with app.test_client() as client:
            url = f"/api/cupcakes/{cupcake.id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {"message": "Deleted"})

            self.assertEqual(Cupcake.query.count(), 1)



  