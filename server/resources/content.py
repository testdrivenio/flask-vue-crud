from flask import make_response
from flask_restful import Resource
from flask import request
from werkzeug.utils import secure_filename
import os
from models.content import ContentModel
from thumbnailGenerator import *
from models.accounts import auth

class Content(Resource):

    def allowed_content(self,filename):
        if not "." in filename:
            return False
        ext = filename.rsplit(".", 1)[1]
        #if ext.upper() in app.config["ALLOWED_CONTENT_EXTENSIONS"]:
        if ext.upper() in ["JPEG", "JPG", "PNG", "GIF","MOV","AVI","PDF","MP4","MKV"]:
            return True
        else:
            return False


    def post(self):
        file = request.files['file']

        save_path = os.path.join('/app/media', secure_filename(file.filename))
        current_chunk = int(request.form['dzchunkindex'])

        # If the file already exists it's ok if we are appending to it,
        # but not if it's new file that would overwrite the existing one
        if os.path.exists(save_path) and current_chunk == 0:
            # 400 and 500s will tell dropzone that an error occurred and show an error
            return make_response(('El fitxer ja existeix a la cartellera', 400))

        try:
            with open(save_path, 'ab') as f:
                f.seek(int(request.form['dzchunkbyteoffset']))
                f.write(file.stream.read())
        except OSError:
            # log.exception will include the traceback so we can see what's wrong
            return make_response(("L'arxiu no s'ha pogut guardar, comprova que estigui conectada la memoria extraible", 500))

        total_chunks = int(request.form['dztotalchunkcount'])

        if current_chunk + 1 == total_chunks:
            # This was the last chunk, the file should be complete and the size we expect
            if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
                log.error(f"File {file.filename} was completed, "
                          f"but has a size mismatch."
                          f"Was {os.path.getsize(save_path)} but we"
                          f" expected {request.form['dztotalfilesize']} ")
                return make_response(('Size mismatch', 500))
            else:
                new_content_file = ContentModel(name=file.filename, path=save_path, size=request.form['dztotalfilesize'])
                new_content_file.save_to_db()
                try:
                    generate_thumbnail(file.filename)
                    print(f'File {file.filename} has been uploaded successfully')
                    make_response(('El fitxer {file.filename} guardat correctament', 200))
                except:
                    print(f'File {file.filename} couldn generate thumbnail')
                    make_response(("No s'ha pogut {file.filename}  generar la miniatura", 400))
                #log.info(f'File {file.filename} has been uploaded successfully')
        #else:
        #print(f'Chunk {current_chunk + 1} of {total_chunks} 'f'for file {file.filename} complete')
        #log.debug(f'Chunk {current_chunk + 1} of {total_chunks} 'f'for file {file.filename} complete')

        return make_response(("Chunk upload successful", 200))

    @auth.login_required()
    def delete(self,id):
        try:
            content = ContentModel.find_by_id(id).json()
            name=content['name']
            response = "El fitxer" + name + "s'ha eliminat correctament"
            ContentModel.delete_by_id(id)
            os.remove(content['path'])
        except:
            m = "No s'ha pogut eliminar el fitxer amb id: " + str(id)
            return {'message': m}, 404
        return {'message': response}, 200

    @auth.login_required()
    def get(self):
        content = ContentModel.query.all()
        container_content = []
        for c in content:
            container_content.append(c.json())
        return {'content': container_content}, 200


