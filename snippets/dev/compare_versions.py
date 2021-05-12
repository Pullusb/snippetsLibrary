## compare versions 
from distutils.version import LooseVersion, StrictVersion
# for software realists
LooseVersion("2.3.1") < LooseVersion("10.1.2")
# for software idealists
StrictVersion("2.3.1") < StrictVersion("10.1.2")