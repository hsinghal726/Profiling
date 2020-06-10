from fds_profiling.report import templates
from fds_profiling.model.aggregators import groupby_aggregator
from fds_profiling.model.charts import bar_chart
from fds_profiling.report import renderable
from fds_profiling.model.describe import describe
from fds_profiling.model.associations import associations

def variables_html(column_types, dataframe, metrics, anchor_id):
    
                
    ## template
    nav_table_template = templates.template("navigation_table.html")
        
    html = ""
    
    for col_i, col_type in column_types.items():
        
        tabs = []
        
        ## 1st tab - describe
        describe_df = describe(dataframe, col_i, col_type)
        
        tabs.append(
            renderable.Renderable(
                content = {
                    "table_1_heading": "Descriptive Statistics",
                    "table_1_content": describe_df,
                    "table_2_heading": "Inferential Statistics",
                    "table_2_content": describe_df
                },
                name = "Descriptive",
                anchor_id = anchor_id + col_i + "describe",
                type_id = "table_table"))
        
        ## 2nd tab - associations
        associations_df = associations(dataframe, col_i, col_type)
        
        tabs.append(
            renderable.Renderable(
                content = {
                    "table_1_heading": "Continuous",
                    "table_1_content": associations_df,
                    "table_2_heading": "Categorical",
                    "table_2_content": associations_df
                },
                name = "Associations",
                anchor_id = anchor_id + col_i + "associations",
                type_id = "table_table"))        
        
        
        ## Remaining tabs - metrics
        agg_df = groupby_aggregator(dataframe, col_i, metrics)
        
        if (col_type == "CAT"):
            
            for metric_i in metrics:
                
                ## a. Table: sorting and re-ordering
                temp_df = agg_df.sort_values(metric_i, ascending=False).head(5)
                temp_df = temp_df[[metric_i] + [col for col in temp_df if col != metric_i]]
                
                ## b. Bar chart:
                bar_chart_encoding = bar_chart(temp_df[metric_i].value_counts())
                
                
                tabs.append(
                    renderable.Renderable(
                        content = {"dataframe": temp_df, "image_encoding": bar_chart_encoding},
                        name = metric_i,
                        anchor_id = anchor_id + col_i + metric_i,
                        type_id = "table_chart"))
                
#                 ## b. Bar chart
#                 tabs.append(
#                     renderable.Renderable(
#                         content = {"image_encoding": },
#                         name = metric_i+"_Chart",
#                         anchor_id = anchor_id + col_i + metric_i + "_Chart",
#                         type_id = "image"))
                
        html += nav_table_template.render(tabs = tabs, anchor_id = anchor_id, header=col_i)
        
    return html
            
