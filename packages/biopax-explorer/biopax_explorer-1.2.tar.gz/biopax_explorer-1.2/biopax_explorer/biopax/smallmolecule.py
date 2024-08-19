 
from biopax.physicalentity import PhysicalEntity
##############################
 


 
from biopax.utils.class_utils import tostring,tojson
from biopax.utils.validate_utils import FullValidateArgType,CValidateArgType,raise_error



validator = FullValidateArgType(raise_error, logger=None)


@tostring
class SmallMolecule(PhysicalEntity) :


    """
    Class SmallMolecule 
    
        
          Definition: A pool of molecules that are neither complexes nor are genetically
      encoded.  Rationale: Identity of small molecules are based on structure, rather
      than sequence as in the case of DNA, RNA or Protein. A small molecule reference
      is a grouping of several small molecule entities  that have the same chemical
      structure.    Usage : Smalle Molecules can have a cellular location and binding
      features. They can't have modification features as covalent modifications of
      small molecules are not considered as state changes but treated as different
      molecules. Some non-genomic macromolecules, such as large complex carbohydrates
      are currently covered by small molecules despite they lack a static structure.
      Better coverage for such molecules require representation of generic
      stoichiometry and polymerization, currently planned for BioPAX level 4.
      Examples: glucose, penicillin, phosphatidylinositol

    
    code generator : rdfobj (author F.Moreews 2023-2024).
    
    """

    ##########constructor

    def __init__(self, *args, **kwargs):
        #args -- tuple of anonymous arguments
        #kwargs -- dictionary of named arguments
        
        self.pk=kwargs.get('pk',None)    
        self.pop_state=kwargs.get('pop_state',None)  
        self.exhausted=kwargs.get('exhausted',None)
        self.meta_label=None  
        
        super().__init__(*args, **kwargs) 
        self.rdf_type="http://www.biopax.org/release/biopax-level3.owl#SmallMolecule"
        self._entityReference=kwargs.get('entityReference',None)  
  

##########getter
     
    def get_entityReference(self):
        """
        Attribute _entityReference  getter
                      Reference entity for this physical entity.

                """
        return self._entityReference  
  
##########setter
    
    @validator(value="biopax.EntityReference", nullable=True, list=True)
    def set_entityReference(self,value):
        self._entityReference=value  
  




    def object_attributes(self):

      object_attribute_list=super().object_attributes() 
      satt=['entityReference']
      for elem in satt:
        object_attribute_list.append(elem)
      return object_attribute_list
 

    def type_attributes(self):
 
      type_attribute_list=super().type_attributes() 
      return type_attribute_list
 
#####get attributes types 
    def attribute_type_by_name(self):
      ma=dict()
      ma=super().attribute_type_by_name() 
      ma['entityReference']='EntityReference'  
      return ma



    def to_json(self):
        return tojson(self)
        

    def get_uri_string(self):
        return self.pk

    def set_uri_string(self,uristr):
        self.pk= uristr       