import logging


class ObjectIO():

    def clear_view_items(parent, tracker):
        if tracker == 'show_layer_names':
            try:
                for layer_list in parent.tracker_dict['show_layer_names']:
                    if layer_list['show']:
                        for item in layer_list['tracking']:
                            parent.view3d.removeItem(item['view'])
                        layer_list['tracking'] = []
            except Exception as e:
                logging.error(f"Failed in `clear_view_items`, {e}")
        else:
            for item in parent.tracker_dict[tracker]:
                parent.view3d.removeItem(item)

            parent.tracker_dict[tracker] = []

    def add_view_items(parent, item_key, tracker):
        parent.view3d.addItem(item_key)

        if isinstance(tracker, tuple) and tracker[0] == 'show_layer_names':
            _, layer_name, site_id, instance = tracker

            for layer_list in parent.tracker_dict['show_layer_names']:
                if layer_name == layer_list['layer_name']:
                    view_dict = {
                        'hole': site_id,
                        'instance': instance,
                        'view': item_key,
                    }
                    layer_list['tracking'].append(view_dict)
        else:
            parent.tracker_dict[tracker].append(item_key)
