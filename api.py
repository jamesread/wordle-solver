#!/usr/bin/env python

import cherrypy
import os
from solver import Solver

class app():
    def __init__(self):
        self.solver = Solver(5)
        self.reset()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def healthz(self):
        return {
            "message": "ready"
        }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def reset(self):
        self.solver.reset()

        return {
            "message": "OK"
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def enterResult(self):
        data = cherrypy.request.json

        print(data)

        for res in data['result']:
            self.solver.addResultLetter(res['character'], res['type'])


        candidates = self.solver.findCandidates()

        for res in data['result']:
            print(res)

        print("Candidates: " + str(len(candidates)))

        candidates = candidates[-9:]

        return {
            "status": "OK",
            "candidates": candidates
        }

if __name__ == "__main__":
    cherrypy.tree.mount(app(), '/', config = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('./frontend'),
            'tools.staticdir.index': 'index.html',
        }
    })

    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.engine.start()
    cherrypy.engine.block()
