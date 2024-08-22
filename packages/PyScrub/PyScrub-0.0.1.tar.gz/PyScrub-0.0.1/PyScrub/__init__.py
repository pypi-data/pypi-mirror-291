# __init__.py inside the Tests/ directory

# Importing all functions from data_cleaning module
from .data_cleaning import (
    handle_missing_values,
    remove_duplicates,
    detect_outliers,
    treat_outliers,
    correct_data_types,
    clean_strings,
    handle_inconsistent_data,
    handle_invalid_data,
    strip_whitespace
)

# Importing all functions from data_transformation module
from .data_transformation import (
    normalize,
    standardize,
    encode_onehot,
    encode_label,
    aggregate,
    summarize,
    extract_features
)

# Importing all functions from feature_engineering module
from .feature_engineering import (
    create_polynomial_features,
    create_interaction_features,
    log_transform,
    boxcox_transform,
    apply_pca,
    select_best_features,
    bin_features,
    create_tfidf_features,
    create_time_series_features
)

# Importing all classes and functions from pipeline_integration module
from .pipeline_integration import (
    DataPipeline,
    PipelineMonitor,
    setup_logging
)

# Importing all functions from visualization module
from .visualization import (
    plot_missing,
    countplot,
    boxplot,
    violinplot,
    histogram,
    scatterplot,
    plot_confusion_matrix,
    plot_auc,
    autoviz
)

from .data_profiler import (
    describe,
    get_cat_feats,
    get_num_feats,
    get_unique_counts,
    display_missing,
    detect_outliers
)