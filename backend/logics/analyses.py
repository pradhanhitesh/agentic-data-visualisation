analyses = {
  "analysis_types": {
    "distribution": {
      "definition": "The representation of how values of one variable are distributed across its range or categories.",
      "use_when": "Analyze a single variable to understand shape, spread, outliers, or frequency.",
      "input_requirement": {
        "num_variables": 1
      },
      "feature_types": ["numeric", "categorical"],
      "tools": {
        "numeric": ["histogram", "boxplot"],
        "categorical": ["bar"]
      }
    },
    "comparison": {
      "definition": "The evaluation of differences in a variable across categories or groups.",
      "use_when": "Compare a metric across different groups or categories.",
      "input_requirement": {
        "num_variables": 2,
        "roles": ["group", "value"]
      },
      "feature_types": {
        "group": "categorical",
        "value": ["numeric", "categorical"]
      },
      "tools": {
        "numeric": ["bar", "boxplot"],
        "categorical": ["grouped_bar"]
      }
    },
    "relationship": {
      "definition": "The analysis of association, correlation, or dependency between two or more variables.",
      "use_when": "Identify trends, correlations, or interactions between variables.",
      "input_requirement": {
        "num_variables": 2
      },
      "feature_types": ["numeric"],
      "tools": {
        "numeric": ["scatter", "regression"]
      }
    },
    "composition": {
      "definition": "The breakdown of a whole into its proportional parts.",
      "use_when": "Show contribution or proportion of categories to a whole.",
      "input_requirement": {
        "num_variables": 1
      },
      "feature_types": ["categorical"],
      "tools": {
        "categorical": ["stacked_bar", "bar"]
      }
    }
  }
}