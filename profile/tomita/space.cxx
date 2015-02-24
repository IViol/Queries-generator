#encoding "utf-8"

#GRAMMAR_ROOT MainRule

// Правило для выделения ФИО
Person -> Word<h-reg1>+[gnc-agr];

// Правило для выделения чисел
Number -> AnyWord<kwtype=number>; // 55

// Правила для выделения дат
Month -> AnyWord<kwtype=month>;
Date -> AnyWord<kwtype=date>+; // 1992 год
Date -> Month AnyWord<kwtype=date>+; // январь 1992 года
Date -> Number Month AnyWord<kwtype=date>+; // 19 января 1992 года

NounFact -> Adj<gnc-agr[1]>* AnyWord<kwtype=noun_fact, gnc-agr[1], rt>; // внеземная цивилизация

AdjFact -> Adj<gnc-agr[1]>* AnyWord<kwtype=adj_fact, gnc-agr[1]> Noun<gnc-agr[1]>*; // земные условия

// Правило для выделения космических объектов. Пример: Орбитальная станция Мир
Object -> Adj<gnc-agr[1]>* AnyWord<rt, gnc-agr[1], kwtype=space_object> Word<h-reg1>* Noun<h-reg1>* Number*;
Earth -> AnyWord<gnc-agr[1]>* Noun<rt, gnc-agr[1], kwtype=earth, h-reg1>;
Planet -> AnyWord<gnc-agr[1]>* Noun<rt, gnc-agr[1], kwtype=planet, h-reg1>;

// Правила для выделения различных видов интеллектуальных открытий, гипотез, и т.д.
Intellect1 -> AnyWord<kwtype=intellectual_discovery> Person<gnc-agr[1]> AnyWord<gnc-agr[1]>*; // Парадокс Энрико Ферми
Intellect2 -> AnyWord<rt, nc-agr[1], kwtype=intellectual_discovery> Noun<nc-agr[1], l-reg>; // гипотеза зоопарка
Intellect3 -> Word<gnc-agr[1], h-reg1> AnyWord<rt, gnc-agr[1], kwtype=intellectual_discovery>; // Манхэттенский проект
Intellect4 -> AnyWord<kwtype=intellectual_discovery> Adj<gnc-agr[1]> Noun<gnc-agr[1]>; // гипотеза уникальной Земли

Human -> AnyWord<gnc-agr[1], kwtype=space_human> Word<h-reg1, gnc-agr[1], rt>+; // физик Энрико Ферми

// космонавт Леонид Кизим и Владимир Соловьев:
Human -> AnyWord<rt, gnc-agr[1], kwtype=space_human> Word<h-reg1, gnc-agr[1]>+ Word<gram="CONJ"> Word<h-reg1, gnc-agr[1]>+;

MainRule -> NounFact interp(SomeFact.some_fact);
MainRule -> AdjFact interp(SomeFact.some_fact::not_norm);
MainRule -> Object interp(ObjectFact.space_object);
MainRule -> Earth interp(ObjectFact.space_object);
MainRule -> Planet interp(ObjectFact.space_object);
MainRule -> Intellect1 interp(IntellectFact.intellectual_discovery);
MainRule -> Intellect2 interp(IntellectFact.intellectual_discovery::not_norm);
MainRule -> Intellect3 interp(IntellectFact.intellectual_discovery);
MainRule -> Intellect4 interp(IntellectFact.intellectual_discovery::not_norm);
MainRule -> Human interp(HumanFact.space_human);
MainRule -> Date interp(DateFact.date);