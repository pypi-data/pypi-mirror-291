import importlib
from functools import wraps
from typepy import String, Integer, Bool, DateTime, RealNumber, TypeConversionError
import builtins

def log_error(msg, func_name, logger):
    logger.log.error('error in %s: %s' % (func_name, msg))
    raise Exception('error in %s: %s' % (func_name, msg))


def raise_error(msg, func_name, logger):
    raise Exception('error in %s: %s' % (func_name, msg))


def ignore_error(msg, func_name, logger):
    pass


class BaseDecorator():
    _error_function = None
    _validation_function = None
    _logger = None

    def __init__(self, validation_function, error_function,
       logger=None 
      ):
        self._validation_function = validation_function
        self._error_function = error_function
        self._logger = logger
 

    __init__.__doc__ = __doc__


class ValidationDecorator(BaseDecorator):
    def __call__(self, **arg_to_check):
        return self._arg_validate(**arg_to_check)

    def _arg_validate(self, validate_func=None, error_func=None, **arg_to_check):
        def on_decorator_call(func):
            all_args = list(func.__code__.co_varnames)

            @wraps(func)
            def on_call(*args, **kwargs):
                positional_args = all_args[:len(args)]
                 
                val=args[positional_args.index("value")]
                 
                msg = ''

                   
                ddict ={
                            'type': None,
                            'val':val,
                            'nullable':True,
                            'list':False,
                            'min':None,
                            'max':None,
                }
                 
                for arg_name, validation_params in arg_to_check.items():
                    if arg_name=='value' :
                        if   isinstance(validation_params, dict) :
                             ddict = validation_params
                        else:
                            
                             ddict['type'] = validation_params 
                    else :
                        ddict[arg_name] = validation_params 

                if self.disable_nullable==True:
                            ddict['nullable']=True
                if self.disable_list==True:
                            ddict['list']=False
                if self.disable_min==True:
                            ddict['min']=None
                if self.disable_max==True:
                            ddict['max']=None 
                #print("::::",ddict)
                msg, _ = self._validation_function( ddict['val'], ddict['type'],
                                                    ddict['nullable'],  ddict['list'] ,
                                                    ddict['min'] ,
                                                    ddict['max']  
                                                    )

                         
                 
                if msg != '':
                        self._error_function(msg, func.__name__, self._logger)
                    
                return func(*args, **kwargs)
            return on_call
        return on_decorator_call





class CValidateArgType(ValidationDecorator):

    def __init__(self, error_function, logger=None,
       disable_nullable=True,                   
       disable_list=True,               
       disable_min=True,            
       disable_max=True
    ):
        self.disable_nullable=disable_nullable                 
        self.disable_list=disable_list                 
        self.disable_min=disable_min               
        self.disable_max=disable_max


        self.allowNone = True # fixme

        super().__init__(self._check_arg_type, error_function, logger)
        self.cmodule = self.init_caster("typepy")

    def init_caster(self, mod):
        cmodule = importlib.import_module(mod)
        globals()[cmodule] = cmodule
        return cmodule

    def split_mod(self, a):
        sep = "."
        cc = a.count(sep)
        if cc == 1:
            return a.split(sep)

        sp = a.split(sep, cc)
        a = sep.join(sp[:cc])
        sb = sp[len(sp)-1:len(sp)]
        b = sep.join(sb)
        return a, b

    def class_for_name(self, module_name, class_name):
        if module_name != '':
           m = importlib.import_module(module_name)
           c = getattr(m, class_name)
        else:
           
           c=  self.get_class_from_string(class_name)
        return c
    
    def get_class_from_string(self,class_name):
               # Try to get the class from the global scope
               if class_name in globals():
                   return globals()[class_name]
    
               # Try to get the class from the built-ins
               if hasattr(builtins, class_name):
                   return getattr(builtins, class_name)
    
               # If the class is not found, return None or raise an error
               raise ValueError(f"Class '{class_name}' not found")

    def _check_arg_type(self, val, type, nullablev=True,list=False,
                         min=None, max=None):
        types = []

        if isinstance(type, str):
            module_name, class_name = self.split_mod(type)
            #print(">>>_check_arg_type>>>>>>>",module_name,class_name)
            if class_name=='Decimal' and (module_name=='' or module_name is None) :
                module_name='decimal' 
                cn = self.class_for_name('decimal', 'Decimal')
                types.append(cn)
                #cn = self.class_for_name('', 'float')
                #types.append(cn)
            else:
                cn = self.class_for_name(module_name, class_name)

                types.append(cn)
        else:
            types.append(type)
         
         
        if nullablev==False and val is None:
             
            msg= 'value is null. not allowed'  

             
            if msg!="":
                 return  msg ,val
        if list:
            return self._check_list_type(val, tuple(types), min, max)
        else:
            return self._check_arg_type_from_class(val, tuple(types))
        

    def conversionClassMapping(self, cl):
        switch = {
            'bool': "Bool",
            'datetime': "DateTime",
            'dict': "Dictionary",
            'list': "List",
            'str': "String",
            'float': "RealNumber",
            'int': "Integer",
        }
        clr = switch.get(cl.__name__, None)
        return clr

    def cast(self, value, conversionClsName, tp):
        class_ = getattr(self.cmodule, conversionClsName)
        instance = class_(value)
        val = instance.force_convert()
        value = tp(val)
        return value

    def _check_arg_type_from_class(self, arg, types):
        msg, value = '', arg
        tp = types[0]
        if value is None and self.allowNone:
            return msg, value

        conversionClsName = self.conversionClassMapping(tp)
        if conversionClsName is not None:
            value = self.cast(value, conversionClsName, tp)

        if not isinstance(value, tp):
            msg = '%s has the type %s, not %s' % (value, type(value), tp)

        return msg, value
 

    def _check_list_type(self, arg, types, min, max):
         
        msg, value = '', arg
        if not isinstance(value, list):
            return '%s is not a list' % value, value

        if (min is not None and len(value) < min) or \
           (max is not None and len(value) > max):
            return 'List cardinality of %s is out of bounds [%s, %s]' % (len(value), min, max), value

        for item in value:
            item_msg, _ = self._check_arg_type_from_class(item, types)
            if item_msg:
                msg += item_msg + '; '

        return msg.strip('; '), value

VALIDATOR_CONFIG = {
    'disable_nullable': True,
    'disable_list': False,
    'disable_min': True,
    'disable_max': True
}

def get_validator_config():
       global VALIDATOR_CONFIG
       return  VALIDATOR_CONFIG

def update_validator_config(new_config):
    global VALIDATOR_CONFIG
    for key in new_config:
        if key in VALIDATOR_CONFIG:
            VALIDATOR_CONFIG[key] = new_config[key]

class FullValidateArgType(CValidateArgType):
    def __init__(self, error_function, logger=None):
        global VALIDATOR_CONFIG
        config = VALIDATOR_CONFIG
        super().__init__(error_function, logger,
                         disable_nullable=config.get('disable_nullable', False),
                         disable_list=config.get('disable_list', False),
                         disable_min=config.get('disable_min', False),
                         disable_max=config.get('disable_max', False))
                        