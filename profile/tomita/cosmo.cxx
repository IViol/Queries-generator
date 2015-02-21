#encoding "utf-8"

#GRAMMAR_ROOT MainRule

Fact     -> AnyWord<kwtype=fact>+;

Object   -> Adj<gnc-agr[1]>* AnyWord<rt, gnc-agr[1], kwtype=object> Word<h-reg1> Noun<h-reg1>*;

IntellectD -> AnyWord<rt, gnc-agr[1], kwtype=inrellect_discovery> Word<h-reg1, gnc-agr[1]>+
  
MainRule -> Fact interp(Fact.fact);
MainRule -> Object interp(Object.object);
MainRule -> IntellectD interp(IntellectD.inrellect_discovery);