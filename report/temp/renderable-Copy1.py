from fds_profiling.report import templates

from fds_profiling.model.aggregators import aggregator

import pandas as pd

class Renderable():
    def __init__(self, content, name, anchor_id, type_id):
        self.content = content
        self.name = name
        self.anchor_id = anchor_id
        self.type_id = type_id

    def render(self):
        
        if ((self.type_id == "nav_table")):
            
            ## template
            nav_table_template = templates.template("navigation_table.html")
        
            html = ""
            for col_i, col_type in self.content['columns_types'].items():
                
                if (col_type == "CAT"):  
                    
                    ## data
                    agg_df = aggregator(self.content['dataframe'], col_i, self.content["metrics"])
                    
                    ## tabs
                    tabs = []
                    for metric_name in self.content["metrics"]:
                        tabs.append(Renderable(content = {"dataframe":agg_df.sort_values(metric_name, ascending=False).head(5)},
                                               name = metric_name,
                                               anchor_id = self.anchor_id+col_i+metric_name,
                                               type_id = "tabs"))
                    html += nav_table_template.render(tabs = tabs, anchor_id = self.anchor_id, header=col_i)
            return html
            
        
        elif (self.type_id == "tabs"):
            df = self.content["dataframe"]
            html_df = df.to_html(classes='freq table table-hover table-striped')
            return html_df
        
        elif (self.type_id == "nav_image"):
            
            ## template
            nav_table_template = templates.template("navigation_table.html")
        
            html = ""
            for col_i, col_type in self.content['columns_types'].items(): 
                ## data
                agg_df = aggregator(self.content['dataframe'], col_i, self.content["metrics"])
                
                ## tabs
                tabs = []
                for metric_name in self.content["metrics"]:
                    tabs.append(
                        Renderable(content = {"dataframe":agg_df.sort_values(metric_name, ascending=False).head(5)},
                                   name = metric_name,
                                   anchor_id = self.anchor_id+col_i+metric_name,
                                   type_id = "tabs"))
                    html += nav_table_template.render(tabs = tabs, anchor_id = self.anchor_id, header=col_i)
            return html
            
            
            
            
            
            ## template
            nav_table_template = templates.template("navigation_table.html")
            
            ## tabs
            tabs = []
            for image_name, image_encoding in self.content["image_encodings"].items():
                tabs.append(
                    Renderable(content = {"dataframe": image_encoding},
                               name = image_name,
                               anchor_id = self.anchor_id+self.name+image_name,
                               type_id = "tabs"))
        
            return nav_table_template.render(tabs = tabs, anchor_id = self.anchor_id)
        
        elif (self.type_id == "image"):
            data = [[self.name,10],['Bob',12],['Clarke',13]]
            df = pd.DataFrame(data,columns=['Name','Age'])
            html_df = df.to_html(classes='freq table table-hover table-striped')
            return html_df
#             return self.content["image_encoding"]
            
        else:
            return ""