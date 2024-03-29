#!venv/bin/python
# -*- coding: utf-8 -*-

import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_apidoc.commands import GenerateApiDoc

basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db)

@manager.command
def test():
    """Run the unit test."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def run_sql():
    sql = "SELECT cp.category_id,c.parent_id FROM fp_category_path AS cp"
    sql += " LEFT JOIN fp_category AS c ON (cp.category_id=c.id)"
    sql += " GROUP BY cp.category_id"
    result = db.engine.execute(sql)

    for row in result:
        print(row)



manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('apidoc', GenerateApiDoc(input_path='app/api_1_0',
                                             output_path='public/docs'))

if __name__ == '__main__':
    manager.run()