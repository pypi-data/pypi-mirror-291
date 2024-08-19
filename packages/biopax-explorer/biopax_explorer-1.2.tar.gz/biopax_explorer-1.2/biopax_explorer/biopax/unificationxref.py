 
from biopax.xref import Xref
##############################
 


 
from biopax.utils.class_utils import tostring,tojson
from biopax.utils.validate_utils import FullValidateArgType,CValidateArgType,raise_error



validator = FullValidateArgType(raise_error, logger=None)


@tostring
class UnificationXref(Xref) :


    """
    Class UnificationXref 
    
        
          Definition: A unification xref defines a reference to an entity in an external
      resource that has the same biological identity as the referring entity
      Rationale: Unification xrefs are critically important for data integration. In
      the future they may be replaced by direct miriam links and rdf:id based identity
      management.   Usage: For example, if one wished to link from a database record,
      C, describing a chemical compound in a BioPAX data collection to a record, C',
      describing the same chemical compound in an external database, one would use a
      unification xref since records C and C' describe the same biological identity.
      Generally, unification xrefs should be used whenever possible, although there
      are cases where they might not be useful, such as application to application
      data exchange.Identity of interactions can be computed based on the  identity of
      its participants. An xref in a protein pointing to a gene, e.g. in the LocusLink
      database17, would not be a unification xref since the two entities do not have
      the same biological identity (one is a protein, the other is a gene). Instead,
      this link should be a captured as a relationship xref. References to an external
      controlled vocabulary term within the OpenControlledVocabulary class should use
      a unification xref where possible (e.g. GO:0005737). Examples: An xref in a
      protein instance pointing to an entry in the Swiss-Prot database, and an xref in
      an RNA instance pointing to the corresponding RNA sequence in the RefSeq
      database..

    
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
        self.rdf_type="http://www.biopax.org/release/biopax-level3.owl#UnificationXref"
  

##########getter
  
##########setter
  




    def object_attributes(self):

      object_attribute_list=super().object_attributes() 
      return object_attribute_list
 

    def type_attributes(self):
 
      type_attribute_list=super().type_attributes() 
      return type_attribute_list
 
#####get attributes types 
    def attribute_type_by_name(self):
      ma=dict()
      ma=super().attribute_type_by_name() 
      return ma



    def to_json(self):
        return tojson(self)
        

    def get_uri_string(self):
        return self.pk

    def set_uri_string(self,uristr):
        self.pk= uristr       