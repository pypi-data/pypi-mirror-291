 
from biopax.entity import Entity
##############################
 


 
from biopax.utils.class_utils import tostring,tojson
from biopax.utils.validate_utils import FullValidateArgType,CValidateArgType,raise_error



validator = FullValidateArgType(raise_error, logger=None)


@tostring
class Interaction(Entity) :


    """
    Class Interaction 
    
        
          Definition: A biological relationship between two or more entities.   Rationale:
      In BioPAX, interactions are atomic from a database modeling perspective, i.e.
      interactions can not be decomposed into sub-interactions. When representing non-
      atomic continuants with explicit subevents the pathway class should be used
      instead. Interactions are not necessarily  temporally atomic, for example
      genetic interactions cover a large span of time. Interactions as a formal
      concept is a continuant, it retains its identitiy regardless of time, or any
      differences in specific states or properties.  Usage: Interaction is a highly
      abstract class and in almost all cases it is more appropriate to use one of the
      subclasses of interaction.  It is partially possible to define generic reactions
      by using generic participants. A more comprehensive method is planned for BioPAX
      L4 for covering all generic cases like oxidization of a generic alcohol.
      Synonyms: Process, relationship, event.  Examples: protein-protein interaction,
      biochemical reaction, enzyme catalysis

    
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
        self.rdf_type="http://www.biopax.org/release/biopax-level3.owl#Interaction"
        self._interactionType=kwargs.get('interactionType',None)  
        self._participant=kwargs.get('participant',None)  
  

##########getter
     
    def get_interactionType(self):
        """
        Attribute _interactionType  getter
                      Controlled vocabulary annotating the interaction type for example,
      "phosphorylation reaction". This annotation is meant to be human readable and
      may not be suitable for computing tasks, like reasoning, that require formal
      vocabulary systems. For instance, this information would be useful for display
      on a web page or for querying a database. The PSI-MI interaction type controlled
      vocabulary should be used. This is browsable at:  http://www.ebi.ac.uk/ontology-
      lookup/browse.do?ontName=MI&termId=MI%3A0190&termName=interaction%20type

                """
        return self._interactionType  
     
    def get_participant(self):
        """
        Attribute _participant  getter
                      This property lists the entities that participate in this interaction. For
      example, in a biochemical reaction, the participants are the union of the
      reactants and the products of the reaction. This property has a number of sub-
      properties, such as LEFT and RIGHT used in the biochemicalInteraction class. Any
      participant listed in a sub-property will automatically be assumed to also be in
      PARTICIPANTS by a number of software systems, including Protege, so this
      property should not contain any instances if there are instances contained in a
      sub-property.

                """
        return self._participant  
  
##########setter
    
    @validator(value="biopax.InteractionVocabulary", nullable=True, list=True, max=1)
    def set_interactionType(self,value):
        self._interactionType=value  
    
    @validator(value="biopax.Entity", nullable=True, list=True)
    def set_participant(self,value):
        self._participant=value  
  




    def object_attributes(self):

      object_attribute_list=super().object_attributes() 
      satt=['interactionType', 'participant']
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
      ma['interactionType']='InteractionVocabulary'  
      ma['participant']='Entity'  
      return ma



    def to_json(self):
        return tojson(self)
        

    def get_uri_string(self):
        return self.pk

    def set_uri_string(self,uristr):
        self.pk= uristr       