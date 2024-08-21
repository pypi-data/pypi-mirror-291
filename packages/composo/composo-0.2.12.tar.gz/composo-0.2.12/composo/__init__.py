_I='CustomStreamWrapper'
_H='Stream'
_G='put'
_F='local'
_E='prod'
_D='PACKAGE_ENV'
_C=False
_B=True
_A=None
__version__='0.2.12'
import datetime,os,atexit,signal,psutil,multiprocessing,dill,signal,inspect,copy,stat,time,json
from typing import List,Union,Any,Literal
from urllib import response
from venv import logger
import requests
from dataclasses import dataclass,asdict
from composo.json_converter import anything_to_python
from composo.package_primitives import*
from composo.helpers import parse_parameters,generate_api_key,parse_return_type,stream_handler,api_key_is_valid
from typing import ClassVar,Dict,Protocol,Any
import multiprocessing,platform,psutil
from functools import wraps
multiprocessing.reduction.ForkingPickler=dill.Pickler
multiprocessing.reduction.dump=dill.dump
def dill_wrapper(func):
	def wrapper(*args,**kwargs):return dill.loads(dill.dumps(func))(*args,**kwargs)
	return wrapper
import logging
from colorama import init,Fore,Style
init()
def is_root_process():return _B;return multiprocessing.current_process().name=='MainProcess'or multiprocessing.parent_process()==_A
def conditional_raise(x):
	'\n    Allow errors to be raised in local\n    '
	if os.environ.get(_D,_E)==_F:raise x
def check_is_jsonable(x):
	recreated_json=json.loads(json.dumps(x))
	if not recreated_json==x:raise ValueError('Result must be parsable JSON')
class ComposoLogHandler(logging.StreamHandler):
	def __new__(cls,*args,**kwargs):return super(ComposoLogHandler,cls).__new__(cls)
	def __init__(self,stream=_A):super().__init__(stream)
	def emit(self,record):
		if record.levelno<=logging.INFO:color=Fore.BLACK
		elif record.levelno==logging.WARNING:color=Fore.YELLOW
		else:color=Fore.RED
		record.msg=f"{Fore.GREEN}Composo:{Style.RESET_ALL}{color} {record.msg}{Style.RESET_ALL}";super().emit(record)
packageLogger=logging.getLogger('ComposoLogger')
if os.environ.get(_D,_E)in[_F,'dev']:print("Using DEBUG logging as you're running locally");packageLogger.setLevel(logging.DEBUG)
else:packageLogger.setLevel(logging.INFO)
if os.environ.get(_D,_E)==_F:packageLogger.info('Connecting to Composo local');BACKEND_URL='http://localhost:8000';FRONTEND_URL='http://localhost:5173'
elif os.environ.get(_D,_E)=='dev':packageLogger.info('Connecting to Composo dev');BACKEND_URL='https://composo-prod-backend-composo-dev-backend.azurewebsites.net';FRONTEND_URL=BACKEND_URL
elif os.environ.get(_D,_E)=='test':packageLogger.info('Connecting to Composo test');BACKEND_URL='http://composo-prod-backend-composo-test-backend.azurewebsites.net';FRONTEND_URL=BACKEND_URL
else:BACKEND_URL='https://app.composo.ai';FRONTEND_URL=BACKEND_URL
handler=ComposoLogHandler()
formatter=logging.Formatter('%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
packageLogger.addHandler(handler)
class IsDataclass(Protocol):__dataclass_fields__:0
def make_request(method,path,data=_A,timeout=100,max_tries=100):
	headers={'Content-Type':'application/json'};url=BACKEND_URL+path;tries=0
	while tries<max_tries:
		try:
			if method.lower()=='post':json_data=json.dumps(asdict(data),default=str);response=requests.post(url,data=json_data,headers=headers,timeout=timeout)
			elif method.lower()=='get':response=requests.get(url,headers=headers,timeout=timeout)
			elif method.lower()==_G:json_data=json.dumps(asdict(data),default=str);response=requests.put(url,data=json_data,headers=headers,timeout=timeout)
			else:raise ValueError('Invalid method. Available options are "post", "get", and "put".')
			if tries>0:packageLogger.info('Connection to Composo backend re-established')
			return response
		except requests.exceptions.Timeout as e:packageLogger.info(f"Request to Composo timed out. Retry {tries+1} of {max_tries}");time.sleep(max(10*(tries/10)**2,10));tries+=1
		except requests.exceptions.ConnectionError as e:packageLogger.info(f"Could not connect to Composo. Retry {tries+1} of {max_tries}");time.sleep(max(10*(tries/10)**2,10));tries+=1
		except Exception as e:raise ComposoDeveloperException(f"There was an unexpected error in make request: {str(e)}")
	raise ComposoDeveloperException(f"Could not connect to Composo backend after {max_tries} tries.")
class BackendEventGress:
	@staticmethod
	def update_last_active(runner_id):make_request(_G,path=f"/api/runner/{runner_id}",data=RunnerUpdate(last_active=datetime.datetime.now(datetime.timezone.utc)))
	def event_poll(self,this_runner_id):
		A='message';response=make_request(method='get',path=f"/api/runner/package/{this_runner_id}")
		if response.status_code==200:
			json_response=response.json()
			try:
				parsed_event=PollResponse(**json_response)
				try:trigger=RunTrigger(**parsed_event.payload);cases=[CaseTrigger(**x)for x in trigger.cases];trigger.cases=cases;parsed_event.payload=trigger;return parsed_event
				except:pass
				try:parsed_event.payload=AppDeletionEvent(**parsed_event.payload);return parsed_event
				except:pass
				parsed_event.payload=_A;return parsed_event
			except Exception as e:raise ComposoDeveloperException(f"Could not parse the response from the backend into a known response type: {response}")
		elif response.status_code==418:packageLogger.error(f"ERROR: {response.json()[A]}")
		elif response.status_code==501:ComposoDeveloperException(f"POLLING ERROR: {response.json()[A]}")
		else:raise ComposoDeveloperException(f"The backend is returning an unknown error from polling: {response}")
	def report_run_results(self,run_result,run_id):
		response=make_request(_G,path=f"/api/runner/package/{run_id}",data=run_result)
		if response.status_code==200:packageLogger.info('Run completed and results reported')
		else:raise ComposoDeveloperException(f"The backend is returning a non 200 status code from reporting run results, this should never happen: {response}")
	def register_runner(self,api_key,adjustable_params,auto_bump,version,docstring):response=make_request('post','/api/runner',data=RunnerCreate(api_key=api_key,parameters=adjustable_params,runner_type='python',package_version=__version__,docstring=docstring,auto_bump=auto_bump,version=version),max_tries=1);return response
def run_experiment(replacement_vars,all_vars,func):
	'\n    Takes a dict replacement_vars where both values are json str dump, conversion to the correct type is handled inside\n    ';packageLogger.info('Experiment initiated')
	if not all(key in[x.name for x in all_vars]for key in replacement_vars.keys()):raise ComposoDeveloperException(f"The user has somehow been allowed to provide args that are not tagged. Provided args: {replacement_vars.keys()}. Tagged args: {[x.name for x in all_vars]} ")
	working_args=[];working_kwargs={}
	for arg in copy.deepcopy(all_vars):
		pushme=lambda x:working_args.append(x)if not arg.is_kwarg else working_kwargs.update({arg.name:x})
		def typeme(x):
			try:return arg.cast(x)
			except Exception as e:raise ComposoUserException(f"The provided arg could not be converted to required type: {arg.param_type}. Arg value was {x}")
		validate_me=lambda x:arg.validate(x)
		if type(arg)==FixedParameter:pushme(arg.live_working_value)
		elif arg.name in replacement_vars:typed=typeme(replacement_vars[arg.name]);validate_me(typed);pushme(typed)
		else:typed=typeme(arg.demo_value);validate_me(typed);pushme(typed)
	try:ret_val=func(*working_args,**working_kwargs)
	except Exception as e:raise ComposoUserException(f"The linked function produced an error: {str(e)}")
	return ret_val
def experiment_controller(func,demo_args,demo_kwargs,demo_globals,api_key='cp-XXX_FAKE_KEY_FOR_TESTING_XXXX',auto_bump=_C,version=_A,event_gress=_A,poll_wait_time=3):
	C='########################################';B='POLL_WAIT_TIME';A='id'
	if os.environ.get(B)is not _A:
		try:_poll_wait_time=int(os.environ.get(B));assert _poll_wait_time>=1 and _poll_wait_time<10;poll_wait_time=_poll_wait_time
		except Exception as e:packageLogger.warning(f"Could not set poll wait time from environment variable: {str(e)}")
	if event_gress is _A:
		if api_key is _A:raise ValueError('api_key must be provided')
		event_gress=BackendEventGress()
	all_vars=parse_parameters(func,*demo_args,**demo_kwargs);return_type=parse_return_type(func);app_is_streaming=return_type in[_H,_I];adjustable_params=[x for x in all_vars if type(x)in WORKABLE_TYPES.__args__];docstring=inspect.getdoc(func);response=event_gress.register_runner(api_key,adjustable_params,auto_bump,version,docstring)
	if response.status_code!=200:raise ComposoDeveloperException(f"Could not register runner: {response.json()}")
	this_runner=response.json();packageLogger.info(C);packageLogger.info('# FOLLOW THE LINK TO REGISTER YOUR APP #');packageLogger.info(f"{Fore.CYAN}"+FRONTEND_URL+'/link?api_key='+api_key+f"{Fore.RESET}");packageLogger.info('######### Or use your API key ##########');packageLogger.info('### '+api_key+' ###');packageLogger.info(C);previously_noted_app_ids=[];packageLogger.info('Connected and listening.')
	while _B:
		try:
			time.sleep(poll_wait_time);BackendEventGress.update_last_active(this_runner[A]);event=event_gress.event_poll(this_runner[A])
			if isinstance(event,PollResponse):
				if isinstance(event.payload,AppDeletionEvent):packageLogger.critical('Composo is shutting down.');packageLogger.critical(event.payload.message);return
				registered_apps=event.registered_apps
				for registered_app in registered_apps:
					if registered_app not in previously_noted_app_ids:packageLogger.info(f"App registered: {registered_app}");previously_noted_app_ids.append(registered_app)
				if event.payload is not _A:
					packageLogger.info('New Evaluation Run Triggered')
					def report_case(case):event_gress.report_run_results(RunResult(run_id=event.payload.run_id,results=[case]),run_id=event.payload.run_id)
					packageLogger.info(f"Running {len(event.payload.cases)} cases")
					for case in event.payload.cases:
						BackendEventGress.update_last_active(this_runner[A]);case_result=_A
						try:
							ret=run_experiment(case.vars,all_vars,func)
							if app_is_streaming:
								if not hasattr(ret,'__iter__'):raise ComposoUserException('The linked function is returning a stream but the return type is not iterable.')
								report_case_intermediate=lambda current_value:report_case(CaseResult(case_id=case.case_id,value=current_value,error=_A,output_stream_incomplete=_B));final_result=stream_handler(ret,report_case_intermediate)
							else:final_result=anything_to_python(ret)
							case_result=CaseResult(case_id=case.case_id,value=final_result,error=_A,output_stream_incomplete=_C);report_case(case_result)
						except ComposoUserException as e:conditional_raise(e);case_result=CaseResult(case_id=case.case_id,value=_A,error='ERROR: '+str(e));report_case(case_result)
						except Exception as e:conditional_raise(e);packageLogger.debug(f"Unidentified exception caught with case {case}: {str(e)}");case_result=CaseResult(case_id=case.case_id,value=_A,error='ERROR: The composo package has failed with an unidentified error. Please contact composo support.');report_case(case_result)
		except ComposoDeveloperException as e:conditional_raise(e);packageLogger.debug(f"Composo Developer Exception caught: {str(e)}");pass
		except ComposoUserException as e:conditional_raise(e);packageLogger.info(f"Composo User Exception caught: {str(e)}")
		except Exception as e:conditional_raise(e);packageLogger.debug(f"Unidentified exception caught: {str(e)}");pass
def error_resistant_composo_server(func,api_key,auto_bump,version,*args,**kwargs):
	A='COMPOSO_APP_API_KEY';packageLogger.info('Composo launched in PID: '+str(os.getpid()))
	try:
		if api_key is _A:
			if A in os.environ:api_key=os.environ[A]
			else:api_key=generate_api_key()
		if not api_key_is_valid(api_key):raise ValueError(f"The provided API key: {api_key} is invalid. Please provide a valid API key.")
		experiment_controller(func,args,kwargs,func.__globals__,api_key=api_key,auto_bump=auto_bump,version=version)
	except Exception as e:packageLogger.error(f"Composo failed to start, or suffered an error from which the server was unable to recover. {str(e)}");return
def process_exists(pid):
	try:return psutil.Process(pid).is_running()
	except psutil.NoSuchProcess:return _C
def error_prone_get_function_unique_id(func):
	source_file=inspect.getsourcefile(func)
	if source_file is _A:raise ComposoDeveloperException('The function could not be detected')
	line_number=inspect.getsourcelines(func)[1]
	if type(line_number)!=int:raise ComposoDeveloperException('The function definiton could not be verified')
	return source_file+str(line_number)
class _Composo:
	_instance=_A;_PERMITTED_RESTART_RATE=1;_initialised=_C;_terminated=_C;_is_root_process=_A;_first_function_id=_A;_server_process=_A;_first_link=_B;_launch_checks_passed=_A;_attempted_start_times=[];disable=_C;api_key=_A;auto_bump=_C;version=_A;development_mode=_C
	def __new__(cls):
		if cls._instance is _A:cls._instance=super().__new__(cls)
		return cls._instance
	def __init__(self):self._server_process=_A;self._watchdog_process=_A;atexit.register(self._cleanup);self._setup_signal_handlers()
	def _setup_signal_handlers(self):signal.signal(signal.SIGTERM,self._signal_handler);signal.signal(signal.SIGINT,self._signal_handler)
	def _signal_handler(self,signum,frame):self._terminated=_B;self._cleanup();os._exit(0)
	def _cleanup(self):
		if self._server_process and self._server_process.pid!=_A and psutil.pid_exists(self._server_process.pid):self._force_terminate_process(self._server_process.pid,'Server')
		if self._watchdog_process and self._watchdog_process.pid!=_A and not psutil.pid_exists(self._server_process.pid)and psutil.pid_exists(self._watchdog_process.pid):self._force_terminate_process(self._watchdog_process.pid,'Watchdog')
	def _force_terminate_process(self,pid,process_name):
		try:process=psutil.Process(pid);process.terminate();process.kill()
		except Exception as e:pass
	def _watchdog(self,server_pid,calling_process_id):
		packageLogger.debug(f"Watchdog process started with PID: {os.getpid()} for Python process PID: {server_pid}")
		while _B:
			if not psutil.pid_exists(calling_process_id)or not psutil.pid_exists(server_pid):
				if psutil.pid_exists(server_pid):
					try:psutil.Process(server_pid).terminate();packageLogger.debug(f"Server process {server_pid} terminated by watchdog")
					except psutil.NoSuchProcess:packageLogger.debug(f"Server process {server_pid} already terminated")
				if not psutil.pid_exists(server_pid):packageLogger.debug(f"Watchdog process {os.getpid()} terminating");os._exit(0)
			time.sleep(.1)
	def link(self,*args,**kwargs):
		for(key,value)in kwargs.items():setattr(self,key,value)
		if self.disable:self.disable=_B;self._terminated=_B;return self
		if self._terminated:return self
		try:self._is_root_process=is_root_process()
		except Exception as e:packageLogger.critical(f"Could not determine if this is the root process: {str(e)}");self._terminated=_B;return self
		if not self._is_root_process:packageLogger.warning('Composo cannot run in a child process. Please run in the main process.');self._terminated=_B;return self
		is_using_mac=platform.system()=='Darwin'
		if not self.development_mode and is_using_mac:packageLogger.critical('development_mode = False is not supported on MacOS, please set development_mode = True');exit()
		self._initialised=_B;return self
	def __call__(self,func):
		@wraps(func)
		def wrapper(*args,**kwargs):
			A='ComposoServer'
			if self._terminated or self.disable:return func(*args,**kwargs)
			try:function_id=error_prone_get_function_unique_id(func)
			except Exception as e:packageLogger.critical(f"Could not get a unique ID for the function: {str(e)}, shutting down.");self._terminated=_B;return func(*args,**kwargs)
			if self._first_function_id is _A:self._first_function_id=function_id
			elif self._first_function_id!=function_id:packageLogger.critical('Composo does not currently support multiple function links in the same codebase, please remove the duplicate decorator');self._terminated=_B;return func(*args,**kwargs)
			else:0
			if self._launch_checks_passed is _A:
				try:self._launch_checks_passed=self.error_prone_passes_launch_checks(func,*args,**kwargs)
				except Exception as e:packageLogger.critical(f"The linked function did not pass the pre-launch checks. Composo will not attempt to retry these, and will shut down. ERROR: {e}");self._terminated=_B;return func(*args,**kwargs)
			if self._launch_checks_passed:
				if self.development_mode:error_resistant_composo_server(func,self.api_key,self.auto_bump,self.version,*args,**kwargs)
				else:
					found_in_children=A in[x.name for x in multiprocessing.active_children()]
					if not found_in_children:
						is_rate_limited=len(self._attempted_start_times)>self._PERMITTED_RESTART_RATE and time.time()-self._attempted_start_times[-self._PERMITTED_RESTART_RATE]<3600;is_on_cooldown=self._attempted_start_times!=[]and time.time()-self._attempted_start_times[-1]<15;was_already_started=self._server_process is not _A;found_root_process=is_root_process();process_is_live=was_already_started and(process_exists(self._server_process.pid)or process_exists(self._watchdog_process.pid))
						if all([found_root_process,self._launch_checks_passed,not is_rate_limited,not is_on_cooldown])and any([not was_already_started,not process_is_live and not found_in_children]):self._attempted_start_times.append(time.time());calling_process_id=os.getpid();packageLogger.debug(f"Launching Composo and Watchdog from PID: {calling_process_id}");self._server_process=multiprocessing.Process(target=dill_wrapper(error_resistant_composo_server),args=(func,self.api_key,self.auto_bump,self.version,*args),kwargs=kwargs,name=A);self._server_process.daemon=_B;self._server_process.start();self._watchdog_process=multiprocessing.Process(target=self._watchdog,args=(self._server_process.pid,calling_process_id),name='ComposoWatchdog');self._watchdog_process.daemon=_B;self._watchdog_process.start()
					return func(*args,**kwargs)
			else:packageLogger.critical('The linked function did not pass the pre-launch checks. Composo will not attempt to retry these, and will shut down.');self._terminated=_B;return func(*args,**kwargs)
		return wrapper
	def error_prone_passes_launch_checks(self,func,*args,**kwargs):
		packageLogger.info('Composo is activated. Running the function once to check for errors...')
		try:first_result=func(*args,**kwargs)
		except Exception as e:packageLogger.critical('The linked function did not pass the pre-launch check: RUN_WITHOUT_ERROR. The function invocation has errors. Error: '+str(e));return _C
		natively_supported_return_types=['int','float','str','dict','list','tuple',_I,_H];result_type=type(first_result).__name__
		if result_type not in natively_supported_return_types:packageLogger.warning(f"The return value of your function: {result_type} is not natively supported by Composo. It will cast to JSON in the Composo platform.")
		STREAM_TYPES=[_H,_I]
		if result_type not in STREAM_TYPES:
			try:anything_to_python(first_result)
			except:packageLogger.critical(f"The linked function did not pass the pre-launch check: RETURN_TYPE. The returned value could not be converted to JSON. The return type was: {result_type}");return _C
		else:0
		packageLogger.info('Function test run successful.');return _B
Composo=_Composo()