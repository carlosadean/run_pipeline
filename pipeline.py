#!/usr/bin/env python

import yaml
import sys
import argparse
from pprint import pprint
import subprocess

#arquivo = open('pipeline.yaml', 'r')
#dados = yaml.load(arquivo)(args.echo)

class Pipeline():
	
	def run_build(self, build, yaml_file='pipeline.yaml'):
		print('pipeline building')
		url = build
		dados_yaml = self.load_yaml(yaml_file)

		cmd = 'git clone %s' % url
		out = self.run_cmd(cmd)
		print(out)

		# - aqui voce pode chamar a funcao run_pipeline(cmd), informando o comando como parametro
		#   note que no pipeline.yaml eu coloquei no build a frase "build fabio's pipeline" e to printando
		#   aqui apenas como exemplo, supondo que essa frase seja o comando que sera executado
		# - eu passo o que esta no pipeline.yaml (build) como argumento para o run_pipeline, que por hora
		#   apenas imprime o conteudo
		"""
		{'branch': 'master',
			'pipelines': [{'build': ['build']},
            	{'release': ['build', 'integration', 'compress']}],
 			'tasks': [{'build': {'cmd': 'mvn clean install'}},
           		{'compress': {'cmd': 'zip -r scripting.zip target/'}},
           		{'integration': {'cmd': 'mvn verify'}}]}

		"""
		build_command_from_yaml = dados_yaml['pipelines'][0]['build'][0]
		pipeline_cmds = self.run_pipeline(build_command_from_yaml)
		print(pipeline_cmds)

		return out

	def load_yaml(self, file):

		arquivo = open('pipeline.yaml', 'r')
		dados = yaml.load(arquivo)

		return dados


	def run_pipeline(self, build_command_from_yaml):
		print('running the pipeline...')
		# aqui tem colocar os comandos do pipeline
		# note que ja criei a funcao run_cmd() que executa comandos do terminal
		# so voce seguir o exemplo que usei do 'git clone' e colocar os comandos
		# do pipeline
		cmd = 'echo %s' % build_command_from_yaml
		out = self.run_cmd(cmd)

		return out

	def run_cmd(self, cmd):
		
		res = subprocess.Popen(cmd, stdout=subprocess.PIPE,
									stderr=subprocess.PIPE,
									shell=True)
		out, err = res.communicate()

		if err:
			print(err)
			sys.exit(1)

		return out

if __name__ == '__main__':
	
	pipeline = Pipeline()

	parser = argparse.ArgumentParser(description="Build a generic product")
	parser.add_argument('-b','--build', type=str, metavar='', required=True, help="inform the url of a git repository")
	args = parser.parse_args()

	# executando a funcao run_build com o endereco informado no argumento
	# pipeline.py --build https://github.com/carlosadean/usbreset.git
	pipeline.run_build(args.build)
