#encoding "utf-8"

#GRAMMAR_ROOT MainRule

Fact     -> AnyWord<kwtype=fact>+;

Object   -> Adj<gnc-agr[1]>* AnyWord<rt, gnc-agr[1], kwtype=object> Word<h-reg1> Noun<h-reg1>*;
  
MainRule -> Fact interp(Fact.fact);
MainRule -> Object interp(Object.object);