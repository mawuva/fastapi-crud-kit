from typing import List, Optional

from .filters.allowed import AllowedFilters


class QueryBuilderConfig:
    """
    Configuration for QueryBuilder with allowed filters validation.
    
    This class holds the configuration for filtering, including which
    filters are allowed and how to handle invalid filters.
    """

    def __init__(
        self,
        allowed_filters: Optional[List[AllowedFilters]] = None,
        ignore_invalid_filters: bool = False,
    ) -> None:
        """
        Initialize QueryBuilder configuration.

        Args:
            allowed_filters: List of AllowedFilters that define which filters are allowed.
                            If None, all filters are allowed (no validation).
            ignore_invalid_filters: If True, invalid filters are silently ignored.
                                   If False, raises an exception for invalid filters.
        """
        self.allowed_filters = allowed_filters or []
        self.ignore_invalid_filters = ignore_invalid_filters

        # Build a mapping from alias/field to AllowedFilters for quick lookup
        self._filter_map: dict[str, AllowedFilters] = {}
        for allowed_filter in self.allowed_filters:
            # Map both the field name and alias to the AllowedFilters instance
            self._filter_map[allowed_filter.field] = allowed_filter
            if allowed_filter.alias != allowed_filter.field:
                self._filter_map[allowed_filter.alias] = allowed_filter

    def get_allowed_filter(self, field_or_alias: str) -> Optional[AllowedFilters]:
        """
        Get the AllowedFilters instance for a given field or alias.

        Args:
            field_or_alias: Field name or alias from the URL

        Returns:
            AllowedFilters instance if found, None otherwise
        """
        return self._filter_map.get(field_or_alias)

    def is_filter_allowed(self, field_or_alias: str) -> bool:
        """
        Check if a filter is allowed.

        Args:
            field_or_alias: Field name or alias to check

        Returns:
            True if the filter is allowed, False otherwise.
            Returns True if no allowed_filters are configured (all filters allowed).
        """
        if not self.allowed_filters:
            return True  # No restrictions, all filters allowed
        return field_or_alias in self._filter_map

