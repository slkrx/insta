import React from 'react';
import PropTypes from 'prop-types';

function Comment(props) {
  const { ownerShowUrl, owner, text } = props;
  return (
    <div className="mb-2">
      <a href={ownerShowUrl} className="me-2">
        { owner }
      </a>
      { text }
    </div>
  );
}

Comment.propTypes = {
  ownerShowUrl: PropTypes.string.isRequired,
  owner: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
};

export default Comment;
