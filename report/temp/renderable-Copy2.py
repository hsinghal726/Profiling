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
        
        if ((self.type_id == "variables")):
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
        
        
        elif (self.type_id == "metric"):
            """
            content:
             - dataframe
             - image_encoding
            """
            
            ## template
            variable_metric_template = templates.template("variable_metric.html")
            
            return variable_metric_template.render(df = self.content["dataframe"], image_encoding = self.content["image_encoding"])
        
        elif (self.type_id == "describe"):
            """
            content:
            """
            ## template
            variable_table_template = templates.template("variable_table.html")
            
            return variable_table_template.render(descriptive_rows = self.content["describe"], inferential_rows = self.content["inference"])
            
            
        
        elif (self.type_id == "condensed_table"):
            """
            content:
             - dataframe   : pandas dataframe             
            """
            
            html = ""
            html += "<div class=\"col-sm-6\">"
            html += "<p class=\"h4\">" + self.content["heading"] + "</p>"
            df = self.content["dataframe"]
            html_df = df.to_html(classes='table table-condensed stats')
            html += html_df + "</div>"
            
            
            html += "<div class=\"col-sm-6\">"
            html += "<p class=\"h4\">" + self.content["heading"] + "</p>"
            df = self.content["dataframe"]
            html_df = df.to_html(classes='table table-condensed stats')
            html += html_df + "</div>"
            
            
            
            return html
        
        elif (self.type_id == "nav_image"):
            
            ## template
            nav_table_template = templates.template("navigation_table.html")
            
            ## tabs
            tabs = []
            for image_name, image_encoding in self.content["image_encodings"].items():
                tabs.append(
                    Renderable(content = {"image_encoding": image_encoding},
                               name = image_name,
                               anchor_id = self.anchor_id + image_name,
                               type_id = "image"))
        
            return nav_table_template.render(tabs = tabs, anchor_id = self.anchor_id)
        
        elif (self.type_id == "image"):
            return self.content["image_encoding"].replace('svg ','svg class="img-responsive center-img"')
            
        else:
            return ""