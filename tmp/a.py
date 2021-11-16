import platform as p
import json

system = p.system()
machine = p.machine()
platform = p.platform()
#uname = list(p.uname())
version = p.version()
arch = p.architecture()
node = p.node()
release = p.release()
pyversion = p.python_version()

d = {
  'system':system,
  'machine':machine,
  'platform':platform,
  'version':version,
  'arch':arch,
  'node':node,
  'release':release,
  'pyversion':pyversion
}

print(json.dumps(d))
