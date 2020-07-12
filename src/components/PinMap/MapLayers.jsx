import React from 'react';
import PropTypes from 'proptypes';
import { REQUEST_TYPES } from '@components/common/CONSTANTS';

class MapLayers extends React.Component {
  onToggleType = id => {
    console.log('toggling:', id);
    const { selectedTypes, onChange } = this.props;

    const newTypes = selectedTypes.includes(id)
      ? selectedTypes.filter(t => t !== id)
      : [ ...selectedTypes, id ];

    onChange(newTypes);
  }

  selectAll = () => {
    this.props.onChange(Object.keys(REQUEST_TYPES));
  }

  deselectAll = () => {
    this.props.onChange([]);
  }

  render() {
    const { selectedTypes } = this.props;
    return (
      <div className="map-layers map-control">
        <div className="type-selectors">
          { Object.keys(REQUEST_TYPES).map(id => {
            const type = REQUEST_TYPES[id];
            const selected = selectedTypes.includes(id);
            return (
              <div
                key={id}
                className="type-selector"
                onClick={this.onToggleType.bind(this, id)}>
                <div
                  className="type-color"
                  style={{
                    backgroundColor: selected ? type.color : 'transparent',
                    borderWidth: selected ? 0 : 1,
                  }}
                />
                <div className="type-name">{ type.displayName }</div>
              </div>
            );
          })}
          <div className="type-selector-buttons">
            <div
              className="type-selector-button"
              onClick={this.selectAll}>
              Select All
            </div>
            <div
              className="type-selector-button"
              onClick={this.deselectAll}>
              Deselect All
            </div>
          </div>
        </div>
      </div>
    );
  }
};

MapLayers.propTypes = {};

MapLayers.defaultProps = {};

export default MapLayers;
