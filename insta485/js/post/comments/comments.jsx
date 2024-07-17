import React from 'react';
import PropTypes from 'prop-types';
import Comment from './comment';
import CreateForm from './createForm';

class Comments extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      comments: [],
      text: '',
    };
    this.onCommentFormEnter = this.onCommentFormEnter.bind(this);
    this.onCommentFormChange = this.onCommentFormChange.bind(this);
  }

  componentDidMount() {
    const { url } = this.props;

    fetch(url, { credentials: 'include' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          comments: data.comments,
        });
      })
      .catch((error) => console.log(error));
  }

  onCommentFormEnter(event) {
    if (event.keyCode !== 13) return;
    event.preventDefault();

    const { url } = this.props;
    const { text } = this.state;

    fetch(url, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState((state) => ({
          comments: state.comments.concat(data),
          text: '',
        }));
      })
      .catch((error) => console.log(error));
  }

  onCommentFormChange(event) {
    this.setState({ text: event.target.value });
  }

  render() {
    const { comments, text } = this.state;
    return (
      <div>
        {comments.map((comment) => (
          <Comment
            key={comment.commentid}
            ownerShowUrl={comment.owner_show_url}
            owner={comment.owner}
            text={comment.text}
          />
        ))}
        <CreateForm
          handleEnter={this.onCommentFormEnter}
          handleChange={this.onCommentFormChange}
          text={text}
        />
      </div>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Comments;
