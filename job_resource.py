from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource

from data.jobs import Jobs
from data import db_session
from data.reqparse_user import parser


def abort_if_jobs_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'is_finished'))})

    def delete(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'is_finished'))
            for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],

        )
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})
