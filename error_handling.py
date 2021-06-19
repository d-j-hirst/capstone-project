from flask import jsonify

def error_400():
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400


def error_404():
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


def error_422():
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
    }), 422


def error_500():
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500

def setup_error_handlers(app):
    @app.errorhandler(400)
    def error_handler_400(error):
        return error_400()

    @app.errorhandler(404)
    def error_handler_404(error):
        return error_404()

    @app.errorhandler(422)
    def error_handler_422(error):
        return error_422()

    @app.errorhandler(500)
    def error_handler_500(error):
        return error_500()
    return app