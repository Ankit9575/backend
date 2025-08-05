from flask import Flask, request, send_file, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/formats', methods=['POST'])
def get_formats():
    data = request.json
    url = data['url']
    ydl_opts = {'quiet': True, 'skip_download': True}
    formats = []
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        for f in info['formats']:
            if f.get('format_id') and f.get('ext') and f.get('format_note'):
                formats.append({
                    'format_id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': f.get('format_note', '')
                })
    return jsonify({'formats': formats})

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data['url']
    format_id = data['format_id']
    filename = 'output.mp4'
    ydl_opts = {
        'format': f'{format_id}+bestaudio/best',
        'outtmpl': filename,
        'merge_output_format': 'mp4',
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
