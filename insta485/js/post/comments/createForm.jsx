import React from 'react';
import PropTypes from 'prop-types';

function CreateForm(props) {
  const { text, handleChange, handleEnter } = props;
  return (
    <form className="comment-form">
      <input
        type="text"
        value={text}
        onChange={handleChange}
        onKeyDown={handleEnter}
        className="form-control"
        placeholder="Add a comment..."
      />
    </form>
  );
}

CreateForm.propTypes = {
  text: PropTypes.string.isRequired,
  handleChange: PropTypes.func.isRequired,
  handleEnter: PropTypes.func.isRequired,
};

export default CreateForm;
