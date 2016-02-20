#!/usr/bin/env python


scoring_rules = {
	"rule-1" : {
		"result" : 0,
		"weightage" : 3.0,
		"standalone-score" : 100,
		"description-score" : "personal information",
	},
	"rule-2" : {
		"result" : 0,
		"weightage" : 7.0,
		"standalone-score" : 100,
		"description-score" : "no of documents submitted"
	},
	"rule-3" : {
		"range" : [36, 45],
		"result" : 0,
		"weightage" : 5.0,
		"standalone-score" : 100,
		"description-score" : "applicant's age"
	},
	"rule-4" : {
		"min-years" : 10,
		"result" : 0,
		"weightage" : 5.0,
		"standalone-score" : 100,
		"description-score" : "no of years in business"
	},
	"rule-5" : {
		"min-percentage" : 50,
		"result" : 0,
		"weightage" : 7.0,
		"standalone-score" : 100,
		"description-score" : "net income percentage of total"
	},
	"rule-6" : {
		"result" : 0,
		"weightage" : 7.0,
		"standalone-score" : 100,
		"description-score" : "no of income sources"
	},
	"rule-7" : {
		"result" : 0,
		"weightage" : 7.0,
		"standalone-score" : 100,
		"description-score" : "net income"
	},
	"rule-8" : {
		"result" : 0,
		"options" : ["Daily", "Monthly", "Yearly"],
		"weightage" : 4.0,
		"standalone-score" : 100,
		"description-score" : "income pattern"
	},
	"rule-9" : {
		"min-transactions" : 80,
		"result" : 0,
		"weightage" : 4.0,
		"standalone-score" : 100,
		"description-score" : "is banking transactions?"
	},
	"rule-10" : {
		"result" : 0,
		"weightage" : 7.0,
		"standalone-score" : 100,
		"description-score" : "what are liabilities?"
	},
	"rule-11" : {
		"result" : 0,
		"weightage" : 7.0,
		"standalone-score" : 100,
		"description-score" : "savings-daily"
	},
	"rule-12" : {
		"result" : 0,
		"min-value" : 50.0,
		"weightage" : 7.0,
		"standalone-score" : 100,
		"description-score" : "what is hypothecation value"
	},
	"rule-13" : {
		"result" : 0,
		"weightage" : 2.0,
		"standalone-score" : 100,
		"description-score" : "seasonality of business"
	},
	"rule-14" : {
		"result" : 0,
		"options" : ["good", "average", "excellent"],
		"weightage" : 8.0,
		"standalone-score" : 100,
		"description-score" : "credit-bureau rating"
	},
	"rule-15" : {
		"result" : 0,
		"options" : ["weak", "strong", "excellent"],
		"weightage" : 5.0,
		"standalone-score" : 100,
		"description-score" : "what is guarantor profile?"
	},
	"rule-16" : {
		"result" : 0,
		"options" : ["weak", "strong", "excellent"],
		"weightage" : 5.0,
		"standalone-score" : 100,
		"description-score" : "what is guarantor feedback?"
	},
	"rule-17" : {
		"result" : 0,
		"max-dependents": 2,
		"weightage" : 1.0,
		"standalone-score" : 100,
		"description-score" : "no of dependents?"
	},
	"rule-18" : {
		"result" : 0,
		"options" : ["own", "rented", "leased"],
		"weightage" : 5.0,
		"standalone-score" : 100,
		"description-score" : "is business premise?"
	},
	"rule-19" : {
		"result" : 0,
		"options" : ["weak", "strong", "excellent"],
		"weightage" : 1.0,
		"standalone-score" : 100,
		"description-score" : "assets land/ flat/ house/ shops/ godown"
	}
}

rule = scoring_rules["rule-1"]
print rule["description-score"]
rule["function"](raw_input())

