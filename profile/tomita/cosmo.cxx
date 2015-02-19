#encoding "utf-8"

#GRAMMAR_ROOT MainRule


Fact     -> AnyWord<kwtype=fact>+;
  
MainRule -> Fact interp(Fact.fact);