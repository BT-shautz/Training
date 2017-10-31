Creating a widget that will be opened through an action (e.g., a custom dashboard) requires the following:
 - A JS file creating the logic of the widget and registering it in the action registry ("static/src/js/dashboard.js").
 - An XML file with the qweb template that will define the widget's GUI ("static/src/xml/widget_templates"). This file
   must be specified in the manifest, via the "qweb" directive.
 - An XML file extending the assets_backend so that it tells Odoo where our JS file is ("assets.xml").
 - An XML file defining the client action that will cause the loading of the widget ("views/dashboard.xml"). The action
   can be called then by a menu item ("views/dashboard.xml").

Creating a widget for a field requires the following:
 - A JS file creating the logic of the widget and registering it in the field registry ("static/src/js/fields.js").
 - An XML file with the qweb template that will define the widget's GUI ("static/src/xml/widget_templates"). This file
   must be specified in the manifest, via the "qweb" directive.
 - An XML file extending the assets_backend so that it tells Odoo where our JS file is ("assets.xml").
 - The widget can then be used in any view using the "widget" attribute of the "field" XML element.
