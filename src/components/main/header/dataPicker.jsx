import React from 'react';
import PropTypes from 'proptypes';

import { YEARS, MONTHS, REQUESTS } from '../../common/CONSTANTS';

const DataPicker = ({
  showMarkers,
  showMarkerDropdown,
  onDropdownSelect,
  toggleShowMarkers,
}) => {
  const handleOnChange = (e) => {
    const { id, value } = e.target;
    onDropdownSelect(id, value);
  };

  const renderDatePicker = () => {
    const options = {
      year: 'Year',
      startMonth: 'Start Month',
      endMonth: 'End Month',
      request: 'Service Requests',
    };

    return Object.keys(options).map((option) => {
      let component;
      const name = options[option];

      switch (name) {
        case 'Year':
          component = YEARS.map((year) => (
            <option key={year} value={year}>
              {year}
            </option>
          ));
          break;
        case 'Start Month':
          component = MONTHS.map((month, idx) => (
            <option key={month} value={idx + 1}>
              {month}
            </option>
          ));
          break;
        case 'End Month':
          component = MONTHS.map((month, idx) => (
            <option key={month} value={idx + 1}>
              {month}
            </option>
          ));
          break;
        case 'Service Requests':
          component = REQUESTS.map((service) => (
            <option key={service} value={service}>
              {service}
            </option>
          ));
          break;
        default:
          break;
      }

      return (
        <React.Fragment key={option}>
          {name}
          &nbsp;
          <select
            id={option}
            className="dropdown"
            defaultValue={option === 'endMonth' ? '12' : null}
            onChange={handleOnChange}
          >
            {component}
          </select>
          <br />
        </React.Fragment>
      );
    });
  };

  return (
    <div className="dropdown-container">
      {renderDatePicker()}
      {showMarkerDropdown && (
        <>
          Show Markers
          <input type="checkbox" value="markers" checked={showMarkers} onChange={toggleShowMarkers} />
        </>
      )}
    </div>
  );
};

DataPicker.propTypes = {
  showMarkerDropdown: PropTypes.bool,
};

DataPicker.defaultProps = {
  showMarkerDropdown: true,
};

export default DataPicker;
