"""Reference synced-folder adapter: save supplied values/files, never retrieve URLs."""
import argparse
import mimetypes
from pathlib import Path
import shutil
import tempfile
import uuid
from capture_store import now, validate_capture, immutable
from ec import Invalid, digest, require, write


def save_capture(inbox, *, value=None, url='', text='', files=(), note='', collections=(), title='',
                 adapter='local-capture', origin='', capture_id=None, captured_at=None):
    inbox=Path(inbox).resolve();inbox.mkdir(parents=True,exist_ok=True)
    cid=capture_id or 'capture-'+uuid.uuid4().hex
    original=value or text or url or ', '.join(Path(p).name for p in files)
    kind='text' if text else 'url' if url else 'file' if files else 'text'
    if len(files)==1:
        mime=mimetypes.guess_type(str(files[0]))[0] or ''
        if mime.startswith('image/'): kind='image'
        if mime.startswith('video/'): kind='video'
    event={'schema_version':'1.0','capture_id':cid,'captured_at':captured_at or now(),
        'original_value':original,'source_type':kind,'capture_status':'captured','processing_status':'pending',
        'provenance':{'adapter':adapter,'origin':origin},'url':url,'shared_text':text,
        'title':title,'user_note':note,'requested_collections':list(collections),'attachments':[]}
    # Validate identity and base fields before using IDs in paths.
    validate_capture(event)
    filenames=[Path(p).name for p in files]
    require(len(filenames)==len(set(filenames)),'Attachments need distinct filenames')
    with tempfile.TemporaryDirectory(prefix='.capture-write-',dir=inbox) as temp:
        staging=Path(temp)
        for source in files:
            source=Path(source);require(source.is_file(),'Shared attachment is not a file')
            raw=source.read_bytes();(staging/source.name).write_bytes(raw)
            event['attachments'].append({'path':f'{cid}/{source.name}','filename':source.name,'byte_size':len(raw),'sha256':digest(raw)})
        validate_capture(event)
        destination=inbox/cid
        if files:
            if destination.exists():
                for a in event['attachments']:
                    require((inbox/a['path']).is_file() and digest((inbox/a['path']).read_bytes())==a['sha256'],'Existing capture attachment differs')
            else: shutil.copytree(staging,destination)
        # Commit marker last. No rewrites of an existing event and no shared append file.
        immutable(inbox/f'{cid}.json',event)
    return inbox/f'{cid}.json'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inbox',required=True);p.add_argument('--value');p.add_argument('--url',default='')
    p.add_argument('--text-file');p.add_argument('--file',action='append',default=[])
    p.add_argument('--note',default='');p.add_argument('--collection',action='append',default=[])
    p.add_argument('--title',default='');p.add_argument('--origin',default='')
    args=p.parse_args()
    try:
        text=Path(args.text_file).read_text(encoding='utf-8-sig') if args.text_file else ''
        print(save_capture(args.inbox,value=args.value,url=args.url,text=text,files=args.file,note=args.note,
              collections=args.collection,title=args.title,origin=args.origin))
    except (OSError,ValueError) as exc: p.exit(1,f'Error: {exc}\n')
