from distutils.core import setup
"""
setup(name='miner',
              py_modules = ['', 'module2']
              packages = ['package1', 'package2']
              scripts = ['script1', 'script2'])
"""
setup(name='miner',
     description='miner: a general purpose rss and social network aggregator',
     author='Mark Menkhus',
     version='0.0.0',
     py_modules = ['miner','miner_site'],
     packages = ['miner'])
