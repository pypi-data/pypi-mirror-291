
'''
	import goodest.goals.umuntu.FDA as FDA_goals_for_umuntu
	goal = FDA_goals_for_umuntu.retrieve ()
'''

'''
	multikey index:
		https://www.mongodb.com/docs/manual/core/indexes/index-types/index-multikey/
'''
def retrieve ():
	return {
		"label": "FDA Goals for Average Adult Homo Sapiens",
		"cautions": [
		  "The goals for each individual adult may vary substantially based on body, lifestyle, and aspirations.",
		  "Consulting with your nutritionist or physician is recommended."
		],
		"ingredients": [
		  {
			"labels": [
			  "Biotin"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "3/100000",
					"decimal string": "3.0000e-5"
				  },
				  "portion": {
					"fraction string": "150/2309920787",
					"percent string": "6.493729172194336e-06"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Calcium"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "13/10",
					"decimal string": "1.3000e+0"
				  },
				  "portion": {
					"fraction string": "6500000/2309920787",
					"percent string": "0.2813949307950879"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Calories"
			],
			"goal": {
			  "energy": {
				"per Earth day": {
				  "Food Calories": {
					"fraction string": "2000",
					"decimal string": "2.0000e+3"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Choline"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "11/20",
					"decimal string": "5.5000e-1"
				  },
				  "portion": {
					"fraction string": "2750000/2309920787",
					"percent string": "0.1190517014902295"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Cholesterol"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "3/10",
					"decimal string": "3.0000e-1"
				  },
				  "portion": {
					"fraction string": "1500000/2309920787",
					"percent string": "0.06493729172194336"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Chromium"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "7/200000",
					"decimal string": "3.5000e-5"
				  },
				  "portion": {
					"fraction string": "175/2309920787",
					"percent string": "7.576017367560059e-06"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Copper"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "9/10000",
					"decimal string": "9.0000e-4"
				  },
				  "portion": {
					"fraction string": "4500/2309920787",
					"percent string": "0.00019481187516583008"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Dietary Fiber"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "28",
					"decimal string": "2.8000e+1"
				  },
				  "portion": {
					"fraction string": "140000000/2309920787",
					"percent string": "6.060813894048048"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Fats"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "78",
					"decimal string": "7.8000e+1"
				  },
				  "portion": {
					"fraction string": "390000000/2309920787",
					"percent string": "16.883695847705276"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Folate",
			  "Folic Acid"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "1/2500",
					"decimal string": "4.0000e-4"
				  },
				  "portion": {
					"fraction string": "2000/2309920787",
					"percent string": "8.658305562925781e-05"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Iodine"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "3/20000",
					"decimal string": "1.5000e-4"
				  },
				  "portion": {
					"fraction string": "750/2309920787",
					"percent string": "3.246864586097168e-05"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Iron"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "9/500",
					"decimal string": "1.8000e-2"
				  },
				  "portion": {
					"fraction string": "90000/2309920787",
					"percent string": "0.003896237503316602"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Magnesium"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "21/50",
					"decimal string": "4.2000e-1"
				  },
				  "portion": {
					"fraction string": "2100000/2309920787",
					"percent string": "0.09091220841072072"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Manganese"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "23/10000",
					"decimal string": "2.3000e-3"
				  },
				  "portion": {
					"fraction string": "11500/2309920787",
					"percent string": "0.0004978525698682325"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Molybdenum"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "9/200000",
					"decimal string": "4.5000e-5"
				  },
				  "portion": {
					"fraction string": "225/2309920787",
					"percent string": "9.740593758291505e-06"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Niacin"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "2/125",
					"decimal string": "1.6000e-2"
				  },
				  "portion": {
					"fraction string": "80000/2309920787",
					"percent string": "0.0034633222251703125"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Pantothenic Acid"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "1/200",
					"decimal string": "5.0000e-3"
				  },
				  "portion": {
					"fraction string": "25000/2309920787",
					"percent string": "0.0010822881953657228"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Phosphorus"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "5/4",
					"decimal string": "1.2500e+0"
				  },
				  "portion": {
					"fraction string": "6250000/2309920787",
					"percent string": "0.27057204884143066"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Potassium"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "47/10",
					"decimal string": "4.7000e+0"
				  },
				  "portion": {
					"fraction string": "23500000/2309920787",
					"percent string": "1.0173509036437793"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Protein"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "50",
					"decimal string": "5.0000e+1"
				  },
				  "portion": {
					"fraction string": "250000000/2309920787",
					"percent string": "10.822881953657227"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Riboflavin"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "13/10000",
					"decimal string": "1.3000e-3"
				  },
				  "portion": {
					"fraction string": "6500/2309920787",
					"percent string": "0.0002813949307950879"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Saturated Fat"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "20",
					"decimal string": "2.0000e+1"
				  },
				  "portion": {
					"fraction string": "100000000/2309920787",
					"percent string": "4.3291527814628905"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Selenium"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "11/200000",
					"decimal string": "5.5000e-5"
				  },
				  "portion": {
					"fraction string": "275/2309920787",
					"percent string": "1.190517014902295e-05"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Sodium"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "23/10",
					"decimal string": "2.3000e+0"
				  },
				  "portion": {
					"fraction string": "11500000/2309920787",
					"percent string": "0.49785256986823245"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Thiamin"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "3/2500",
					"decimal string": "1.2000e-3"
				  },
				  "portion": {
					"fraction string": "6000/2309920787",
					"percent string": "0.00025974916688777344"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "carbohydrates"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "275",
					"decimal string": "2.7500e+2"
				  },
				  "portion": {
					"fraction string": "1375000000/2309920787",
					"percent string": "59.52585074511475"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Vitamin A"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "9/10000",
					"decimal string": "9.0000e-4"
				  },
				  "portion": {
					"fraction string": "4500/2309920787",
					"percent string": "0.00019481187516583008"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Vitamin B6"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "17/10000",
					"decimal string": "1.7000e-3"
				  },
				  "portion": {
					"fraction string": "8500/2309920787",
					"percent string": "0.0003679779864243457"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Vitamin B12"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "3/1250000",
					"decimal string": "2.4000e-6"
				  },
				  "portion": {
					"fraction string": "12/2309920787",
					"percent string": "5.194983337755469e-07"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Vitamin C"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "9/100",
					"decimal string": "9.0000e-2"
				  },
				  "portion": {
					"fraction string": "450000/2309920787",
					"percent string": "0.01948118751658301"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Vitamin D"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "1/50000",
					"decimal string": "2.0000e-5"
				  },
				  "portion": {
					"fraction string": "100/2309920787",
					"percent string": "4.3291527814628905e-06"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Vitamin E"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "3/200",
					"decimal string": "1.5000e-2"
				  },
				  "portion": {
					"fraction string": "75000/2309920787",
					"percent string": "0.003246864586097168"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Vitamin K"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "3/25000",
					"decimal string": "1.2000e-4"
				  },
				  "portion": {
					"fraction string": "600/2309920787",
					"percent string": "2.5974916688777345e-05"
				  }
				}
			  }
			}
		  },
		  {
			"labels": [
			  "Zinc"
			],
			"goal": {
			  "mass + mass equivalents": {
				"per Earth day": {
				  "grams": {
					"fraction string": "11/1000",
					"decimal string": "1.1000e-2"
				  },
				  "portion": {
					"fraction string": "55000/2309920787",
					"percent string": "0.00238103402980459"
				  }
				}
			  }
			}
		  }
		],
		"limiters": [
		  {
			"label": "species",
			"includes": [
			  "human"
			]
		  },
		  {
			"kind": "slider--integer",
			"label": "age",
			"includes": [
			  [
				"20",
				"eternity"
			  ]
			]
		  },
		  {
			"label": "exclusions",
			"includes": [
			  "pregnant",
			  "breast feeding"
			]
		  }
		],
		"sources": [
		  "https://www.fda.gov/food/new-nutrition-facts-label/daily-value-new-nutrition-and-supplement-facts-labels",
		  "https://www.fda.gov/food/nutrition-facts-label/calories-nutrition-facts-label",
		  "https://www.fda.gov/media/99069/download",
		  "https://www.fda.gov/media/99059/download"
		],
		"statistics": {
		  "sum": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "2309920787/5000000",
				  "decimal string": "461.9841574"
				}
			  }
			}
		  }
		}
	  }

