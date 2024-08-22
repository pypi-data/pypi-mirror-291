Changelog
=========

0.0.4 (2024-08-22)
------------------

- method `_object_from_dict` (`opex.ObjectPredictions`) now handles incorrect
  `score` values better
- method `to_dict` (`opex.ObjectPrediction`) only returns the score when not
  `None`; meta-data is returned now as well


0.0.3 (2024-08-12)
------------------

- method `_from_dict` (`opex.ObjectPredictions`) no longer raises an Exception
  when the timestamp is missing
- method `to_dict` (`opex.ObjectPredictions`) only returns timestamp/meta
  when not None now


0.0.2 (2024-06-17)
------------------

- proper integration of orjson (uses bytes instead of strings)


0.0.1 (2024-06-14)
------------------

- initial release
