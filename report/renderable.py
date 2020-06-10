import pandas as pd
from fds_profiling.report import templates

from fds_profiling.model.aggregators import groupby_aggregator
from fds_profiling.report.variables import variables_html

class Renderable():
    def __init__(self, content, name, anchor_id, type_id):
        self.content = content
        self.name = name
        self.anchor_id = anchor_id
        self.type_id = type_id
        
    def render(self):
        
        if ((self.type_id == "variables_container")):
            """
            content:
             - column_types: dict(column_name, column_type)
             - dataframe   : pandas dataframe
             - metrics     : list(metrics)
             
            """
            return variables_html(self.content["column_types"], self.content["dataframe"], self.content["metrics"], self.anchor_id)
            
        elif (self.type_id == "table"):
            df = self.content["dataframe"]
            html_df = df.to_html(classes='table table-condensed stats freq table-hover table-striped')
            return html_df
        
        
        elif (self.type_id == "table_chart"):
            """
            content:
             - dataframe
             - image_encoding
            """
            
            ## template
            variable_metric_template = templates.template("table_chart.html")
            
            return variable_metric_template.render(df = self.content["dataframe"], image_encoding = self.content["image_encoding"])
        
        elif (self.type_id == "table_table"):
            """
            content:
             - table_1_heading
             - table_1_content: dictionary
             - table_2_heading
             - table_2_content: dictionary
            """
            ## template
            variable_table_template = templates.template("table_table.html")
            
            return variable_table_template.render(
                table_1_heading = self.content["table_1_heading"],
                table_1_content = self.content["table_1_content"],
                table_2_heading = self.content["table_2_heading"],
                table_2_content = self.content["table_2_content"])

        
        elif (self.type_id == "image"):
            return self.content["image_encoding"].replace('svg ','svg class="img-responsive center-img"')
            
        else:
            return ""